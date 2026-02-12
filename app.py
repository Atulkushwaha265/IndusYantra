from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Machine, Enquiry
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Database configuration - Force SQLite for local development
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///b2b_platform.db')

# Debug: Print environment variables
print(f"Raw DATABASE_URL from env: {os.getenv('DATABASE_URL')}")
print(f"Final DATABASE_URL: {DATABASE_URL}")

# Force SQLite for local development to avoid database issues
if not DATABASE_URL or 'hotel_db' in DATABASE_URL:
    print("Forcing SQLite for local development...")
    DATABASE_URL = 'sqlite:///b2b_platform.db'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create upload directories if they don't exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_images'), exist_ok=True)

db.init_app(app)

# Helper functions
def is_logged_in():
    return 'user_id' in session

def get_current_user():
    if is_logged_in():
        return db.session.get(User, session['user_id'])
    return None

def login_required(f):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not is_logged_in():
                flash('Please login to access this page', 'error')
                return redirect(url_for('login'))
            
            user = get_current_user()
            if user.role not in allowed_roles:
                flash('You do not have permission to access this page', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

# Routes
@app.route('/')
def home():
    """Home page - displays featured machines"""
    featured_machines = Machine.query.order_by(Machine.created_at.desc()).limit(6).all()
    return render_template('home.html', machines=featured_machines)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Validation
        if not all([name, email, password, role]):
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=password_hash, role=role)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            session['user_profile_image'] = user.profile_image
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard"""
    user = get_current_user()
    
    # Double-check if user exists (handle session issues)
    if not user:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))
    
    if user.role == 'supplier':
        # Supplier dashboard - show their machines and enquiries
        machines = Machine.query.filter_by(supplier_id=user.id).all()
        machine_ids = [m.id for m in machines]
        enquiries = Enquiry.query.filter(Enquiry.machine_id.in_(machine_ids)).order_by(Enquiry.created_at.desc()).all()
        return render_template('dashboard_supplier.html', user=user, machines=machines, enquiries=enquiries)
    
    elif user.role == 'buyer':
        # Buyer dashboard - show their enquiries
        enquiries = Enquiry.query.filter_by(buyer_id=user.id).order_by(Enquiry.created_at.desc()).all()
        return render_template('dashboard_buyer.html', user=user, enquiries=enquiries)
    
    elif user.role == 'admin':
        # Admin dashboard - show overview
        total_users = User.query.count()
        total_machines = Machine.query.count()
        total_enquiries = Enquiry.query.count()
        recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(10).all()
        return render_template('dashboard_admin.html', user=user, 
                             total_users=total_users, total_machines=total_machines, 
                             total_enquiries=total_enquiries, recent_enquiries=recent_enquiries)
    
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = get_current_user()
    
    # Double-check if user exists (handle session issues)
    if not user:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))
    
    # Get additional data for profile
    if user.role == 'supplier':
        machines_count = Machine.query.filter_by(supplier_id=user.id).count()
        machine_ids = [m.id for m in Machine.query.filter_by(supplier_id=user.id).all()]
        enquiries_count = Enquiry.query.filter(Enquiry.machine_id.in_(machine_ids)).count()
    else:
        machines_count = 0
        enquiries_count = Enquiry.query.filter_by(buyer_id=user.id).count()
    
    return render_template('profile.html', user=user, machines_count=machines_count, enquiries_count=enquiries_count)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    user = get_current_user()
    
    # Double-check if user exists (handle session issues)
    if not user:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Update user profile
        user.name = request.form.get('name', user.name)
        user.company_name = request.form.get('company_name', user.company_name)
        user.city = request.form.get('city', user.city)
        user.industry = request.form.get('industry', user.industry)
        user.phone = request.form.get('phone', user.phone)
        
        # Handle profile image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '' and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                # Add user ID and timestamp to make it unique
                unique_filename = f"user_{user.id}_{int(datetime.utcnow().timestamp())}_{filename}"
                
                # Save the file
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'profile_images', unique_filename)
                file.save(upload_path)
                
                # Update user profile image path (relative to static folder)
                user.profile_image = f'uploads/profile_images/{unique_filename}'
                
                # Delete old profile image if it exists
                if user.profile_image and user.profile_image != f'uploads/profile_images/{unique_filename}':
                    old_path = os.path.join('static', user.profile_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=user)

@app.route('/machines')
def machines_list():
    """List all machines with filtering"""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Machine.query
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Machine.name.ilike(f'%{search}%') | 
                           Machine.description.ilike(f'%{search}%'))
    
    machines = query.order_by(Machine.created_at.desc()).all()
    categories = db.session.query(Machine.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('machines_list.html', machines=machines, categories=categories, 
                         selected_category=category, search_query=search)

@app.route('/machine/<int:machine_id>')
def machine_detail(machine_id):
    """Machine detail page with fully dynamic content"""
    machine = Machine.query.get_or_404(machine_id)
    supplier = User.query.get(machine.supplier_id)
    
    # Get additional supplier stats
    supplier_machines_count = Machine.query.filter_by(supplier_id=supplier.id).count()
    
    # Get all enquiries for this machine (for buyer context)
    machine_enquiries = Enquiry.query.filter_by(machine_id=machine.id).all()
    
    return render_template('machine_detail.html', 
                         machine=machine, 
                         supplier=supplier,
                         supplier_machines_count=supplier_machines_count,
                         machine_enquiries=machine_enquiries)

@app.route('/add-machine', methods=['GET', 'POST'])
@login_required
@role_required('supplier')
def add_machine():
    """Add new machine (supplier only)"""
    if request.method == 'POST':
        # Basic Information
        name = request.form.get('name')
        category = request.form.get('category')
        use_case = request.form.get('use_case')
        price_range = request.form.get('price_range')
        description = request.form.get('description')
        
        # Technical Specifications
        production_capacity = request.form.get('production_capacity')
        automation_level = request.form.get('automation_level')
        power_requirement = request.form.get('power_requirement')
        machine_dimensions = request.form.get('machine_dimensions')
        raw_material = request.form.get('raw_material')
        operator_skill = request.form.get('operator_skill')
        warranty_info = request.form.get('warranty_info')
        
        # Business Fit Information
        ideal_industry = request.form.get('ideal_industry')
        business_size_fit = request.form.get('business_size_fit')
        installation_support = request.form.get('installation_support')
        
        # Multiple Images
        image_front = request.form.get('image_front')
        image_side = request.form.get('image_side')
        image_working = request.form.get('image_working')
        image_closeup = request.form.get('image_closeup')
        
        # Validation
        if not all([name, category, use_case, price_range, description]):
            flash('All basic fields are required', 'error')
            return render_template('add_machine.html')
        
        # At least one image is required
        if not any([image_front, image_side, image_working, image_closeup]):
            flash('At least one machine image is required', 'error')
            return render_template('add_machine.html')
        
        # Create machine object
        machine = Machine(
            supplier_id=session['user_id'],
            name=name,
            category=category,
            use_case=use_case,
            price_range=price_range,
            description=description,
            production_capacity=production_capacity,
            automation_level=automation_level,
            power_requirement=power_requirement,
            machine_dimensions=machine_dimensions,
            raw_material=raw_material,
            operator_skill=operator_skill,
            warranty_info=warranty_info,
            ideal_industry=ideal_industry,
            business_size_fit=business_size_fit,
            installation_support=installation_support,
            image_front=image_front,
            image_side=image_side,
            image_working=image_working,
            image_closeup=image_closeup
        )
        
        try:
            db.session.add(machine)
            db.session.commit()
            flash('Machine added successfully!', 'success')
            return redirect(url_for('machine_detail', machine_id=machine.id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add machine. Please try again.', 'error')
            print(f"Error adding machine: {e}")
    
    return render_template('add_machine.html')

@app.route('/enquiry/<int:machine_id>', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def create_enquiry(machine_id):
    """Create enquiry for a machine (buyer only)"""
    machine = Machine.query.get_or_404(machine_id)
    
    if request.method == 'POST':
        message = request.form.get('message')
        budget = request.form.get('budget')
        location = request.form.get('location')
        production_need = request.form.get('production_need')
        timeline = request.form.get('timeline', 'planning')  # Default to planning
        
        if not all([message, budget, location, production_need]):
            flash('All fields except timeline are required', 'error')
            return render_template('enquiry_form.html', machine=machine)
        
        enquiry = Enquiry(
            buyer_id=session['user_id'],
            machine_id=machine_id,
            message=message,
            budget=budget,
            location=location,
            production_need=production_need
        )
        
        try:
            db.session.add(enquiry)
            db.session.commit()
            flash('Enquiry sent successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to send enquiry. Please try again.', 'error')
    
    return render_template('enquiry_form.html', machine=machine)

@app.route('/enquiries')
@login_required
@role_required('supplier')
def view_enquiries():
    """View enquiries for supplier's machines"""
    user = get_current_user()
    machines = Machine.query.filter_by(supplier_id=user.id).all()
    machine_ids = [m.id for m in machines]
    enquiries = Enquiry.query.filter(Enquiry.machine_id.in_(machine_ids)).order_by(Enquiry.created_at.desc()).all()
    
    return render_template('enquiries_list.html', enquiries=enquiries, machines=machines)

# Create database tables
try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
except Exception as e:
    print(f"Database initialization error: {e}")
    print("Application will start, but database operations may fail.")

if __name__ == '__main__':
    print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True)
