import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

razorpay_client = razorpay.Client(
    auth=(
        os.getenv('RAZORPAY_KEY_ID'), 
        os.getenv('RAZORPAY_KEY_SECRET')
        )
    )
razorpay_client.enable_retry(True) 

razorpay_client.set_app_details({"title":"FoodieFreak", "version":"1.0.0"}) 