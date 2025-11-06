# E-Commerce M-Pesa Paybill Integration

## Requirements (requirements.txt)

```txt
Django>=4.2
python-decouple>=3.8
requests>=2.31.0
Pillow>=10.0.0
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env` File

Create a `.env` file in your project root with the following:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_CALLBACK_URL=https://your-ngrok-url.ngrok.io/mpesa/callback/
```

### 3. Create Logs Directory

```bash
mkdir logs
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Setup Ngrok (for local testing)

M-Pesa callback requires a public HTTPS URL. Use ngrok:

```bash
# Install ngrok from https://ngrok.com/
# Run your Django server
python manage.py runserver

# In another terminal, run ngrok
ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
# Update .env file:
MPESA_CALLBACK_URL=https://abc123.ngrok.io/mpesa/callback/
```

### 7. Get M-Pesa Credentials

1. Go to [Safaricom Daraja Portal](https://developer.safaricom.co.ke/)
2. Create an account
3. Create a new app
4. Get your **Consumer Key** and **Consumer Secret**
5. Get your **Passkey** from the app settings
6. For sandbox testing, use:
   - Shortcode: `174379`
   - Test Phone: `254708374149`

### 8. Register Callback URLs

In the Daraja Portal:
1. Go to your app settings
2. Register your callback URL
3. Format: `https://your-domain.com/mpesa/callback/`

## Project Structure

```
your_project/
├── store/
│   ├── models.py          # Database models
│   ├── views.py           # Views with M-Pesa integration
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   └── templates/
│       └── store/
│           ├── checkout.html
│           ├── product_list.html
│           ├── cart.html
│           └── order_detail.html
├── logs/                  # Log files
├── media/                 # Product images
├── static/                # CSS, JS files
├── .env                   # Environment variables
├── manage.py
└── requirements.txt
```

## Testing M-Pesa Payment (Sandbox)

### Test Credentials
- **Phone Number**: 254708374149
- **Paybill**: 174379
- **Account Number**: Any (e.g., ACC001)
- **Amount**: 1-70000 KSh

### Testing Flow

1. Add products to cart
2. Go to checkout
3. Enter phone number: `254708374149`
4. Enter account number: `ACC001` (or any)
5. Enter delivery address
6. Click "Pay with M-Pesa"
7. Check your phone for STK push prompt
8. Enter PIN shown on phone
9. Wait for confirmation

### Monitoring Logs

```bash
tail -f logs/mpesa.log
```

## Production Deployment

### 1. Update Environment

```env
MPESA_ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

### 2. Get Production Credentials

1. Apply for Production access in Daraja Portal
2. Get production Consumer Key & Secret
3. Get production Passkey
4. Register production callback URL

### 3. Update Settings

Replace sandbox credentials with production credentials in `.env`

### 4. SSL Certificate

Ensure your domain has a valid SSL certificate (required for M-Pesa callbacks)

### 5. Register URLs

Register these URLs with Safaricom:
- **Callback URL**: `https://yourdomain.com/mpesa/callback/`
- **Validation URL**: (optional)
- **Timeout URL**: (optional)

## Admin Panel

Access admin at: `http://localhost:8000/admin/`

You can:
- Add/Edit products
- View orders
- Check M-Pesa payment status
- Monitor transactions

## Troubleshooting

### Callback not working
- Ensure ngrok is running
- Check callback URL is correct in .env
- Verify URL is registered in Daraja Portal
- Check logs: `logs/mpesa.log`

### STK Push not received
- Verify phone number format (254XXXXXXXXX)
- Check phone has active M-Pesa
- Try sandbox test number: 254708374149
- Check internet connection

### Payment stuck on "Processing"
- Check M-Pesa callback logs
- Verify callback URL is accessible
- Check if payment was completed manually

### Access Token Error
- Verify Consumer Key & Secret
- Check internet connection
- Verify Daraja Portal credentials

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products/` | GET | List all products |
| `/product/<id>/` | GET | Product details |
| `/cart/` | GET | View cart |
| `/cart/add/<id>/` | POST | Add to cart |
| `/checkout/` | GET, POST | Checkout & payment |
| `/mpesa/callback/` | POST | M-Pesa callback |
| `/check-payment-status/<id>/` | GET | Check payment status |
| `/orders/` | GET | List user orders |
| `/order/<id>/` | GET | Order details |

## Security Notes

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use environment variables** for all sensitive data
3. **Enable HTTPS** in production
4. **Validate callback signatures** (optional enhancement)
5. **Rate limit** payment endpoints
6. **Log all transactions** for auditing

## Support

- Safaricom Daraja: support@safaricom.co.ke
- Documentation: https://developer.safaricom.co.ke/docs