from fastapi import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from redis.exceptions import RedisError



class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client, limit:int=100, window:int=60):
        super().__init__(app)
        self.app = app
        self.redis = redis_client
        self.limit = limit 
        self.window = window
        
        #script for redis operation 
        self.script = """
            local count = redis.call('INCR', KEYS[1])
            
            if count == 1 then
                redis.call('EXPIRE', KEYS[1], ARGV[1])
            end
            
            local ttl = redis.call('TTL', KEYS[1])
            
            return {count, ttl}
        """
        
    async def dispatch(self, request:Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        
        redis_key = f"rate_limit:{client_ip}"
        try:
            result = await self.redis.eval(
                self.script, 1, redis_key, self.window
            )
            request_count = int(result[0])
            ttl = int(result[1])
            
            
        except RedisError:
            return JSONResponse(
                status_code=503, content={"detail": "Rate limiter temporarily unavailable"}
            )
            
        if request_count > self.limit:
            return JSONResponse(
                status_code=429, content={"detail": "Too many requests. Try again later."},
                headers={
                    "Retry-After": str(max(ttl, 0)),
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Remaining": "0"
                }
            ) 
        
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, self.limit - request_count))

        return response
    