# B2B Manufacturing Platform

A complete full-stack web application that connects MSME buyers with machine suppliers. This platform acts as an intermediate discovery and enquiry system between MSMEs and machine suppliers.

## Features

- **User Authentication**: Role-based login system (Buyer, Supplier, Admin)
- **Machine Listings**: Suppliers can list their machines with detailed information
- **Enquiry System**: Buyers can send enquiries to suppliers about specific machines
- **Dashboard**: Role-based dashboards for different user types
- **Search & Filter**: Browse machines by category and search functionality
- **Responsive Design**: Clean, minimal UI that works on all devices

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: Session-based (Werkzeug)

## Project Structure

```
B2B/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables example
├── README.md             # This file
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── machines_list.html
│   ├── machine_detail.html
│   ├── add_machine.html
│   ├── enquiry_form.html
│   ├── dashboard_supplier.html
│   ├── dashboard_buyer.html
│   ├── dashboard_admin.html
│   └── enquiries_list.html
└── static/
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── script.js     # Frontend JavaScript
```

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd B2B
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/b2b_platform

# Flask Secret Key
SECRET_KEY=your-secret-key-change-this-in-production
```

### Step 5: Set Up PostgreSQL Database

1. Install PostgreSQL on your system
2. Create a database:

```sql
CREATE DATABASE b2b_platform;
```

3. Update the `DATABASE_URL` in your `.env` file with your PostgreSQL credentials

### Step 6: Initialize the Database

Run the Flask application to create the database tables:

```bash
python app.py
```

The application will automatically create the necessary tables on first run.

### Step 7: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Database Schema

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: User's email (unique)
- `password_hash`: Hashed password
- `role`: User role ('buyer', 'supplier', 'admin')
- `created_at`: Registration timestamp

### Machines Table
- `id`: Primary key
- `supplier_id`: Foreign key to users table
- `name`: Machine name
- `category`: Machine category
- `use_case`: Intended use case
- `price_range`: Price range
- `description`: Detailed description
- `image_url`: URL to machine image
- `created_at`: Listing timestamp
- `updated_at`: Last update timestamp

### Enquiries Table
- `id`: Primary key
- `buyer_id`: Foreign key to users table
- `machine_id`: Foreign key to machines table
- `message`: Enquiry message
- `budget`: Buyer's budget
- `location`: Buyer's location
- `production_need`: Production requirements
- `status`: Enquiry status ('pending', 'responded', 'closed')
- `created_at`: Enquiry timestamp

## User Roles and Permissions

### Buyer (MSME)
- Browse all machines
- Send enquiries to suppliers
- View own enquiries
- Access buyer dashboard

### Supplier
- Add/edit machine listings
- View enquiries for their machines
- Respond to buyer enquiries
- Access supplier dashboard

### Admin
- View platform statistics
- Monitor all activities
- Access admin dashboard

## Deployment on Render

### Step 1: Prepare for Deployment

1. Create a GitHub repository and push your code
2. Ensure your `requirements.txt` is complete
3. Set up PostgreSQL on Render

### Step 2: Create Render Services

1. **PostgreSQL Database**:
   - Go to Render Dashboard
   - Create new PostgreSQL instance
   - Choose a plan (free tier available)
   - Note the database connection string

2. **Web Service**:
   - Create new Web Service
   - Connect your GitHub repository
   - Set environment variables:
     - `DATABASE_URL`: Your PostgreSQL connection string
     - `SECRET_KEY`: Generate a secure random string

### Step 3: Configure Render Web Service

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
python app.py
```

**Environment Variables**:
- `DATABASE_URL`: `postgresql://username:password@host:port/database`
- `SECRET_KEY`: Your secret key

### Step 4: Deploy

1. Push your code to GitHub
2. Render will automatically build and deploy
3. Your application will be available at the provided URL

## Important Notes

### Security Considerations

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Validate all user inputs
- Implement rate limiting for forms
- Regularly update dependencies

### Performance Optimization

- Add database indexes for frequently queried fields
- Implement pagination for large datasets
- Optimize image sizes
- Consider caching for static content

### Scaling Considerations

- Use a managed PostgreSQL service for production
- Implement proper logging and monitoring
- Set up backup strategies
- Consider CDN for static assets

## Common Issues and Solutions

### Database Connection Issues

1. **Connection refused**: Check if PostgreSQL is running
2. **Authentication failed**: Verify database credentials
3. **Database doesn't exist**: Create the database manually

### Import Errors

1. **Module not found**: Activate virtual environment
2. **Version conflicts**: Update requirements.txt
3. **SQLAlchemy errors**: Check database URL format

### Template Errors

1. **Template not found**: Check file paths in templates folder
2. **Variable not defined**: Check context variables in routes
3. **Syntax errors**: Validate Jinja2 template syntax

## Development Tips

### Adding New Features

1. Update models.py for database changes
2. Add routes in app.py
3. Create corresponding templates
4. Update CSS and JavaScript as needed

### Testing

1. Test all user roles and permissions
2. Verify form validations
3. Test database operations
4. Check responsive design

### Debugging

1. Enable Flask debug mode in development
2. Check browser console for JavaScript errors
3. Review Flask logs for server errors
4. Use database logs for SQL issues

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with different user roles
4. Verify database connections

## License

This project is open-source and available under the MIT License.
