#!/usr/bin/env python3
"""
Database initialization script for B2B Manufacturing Platform
Run this script to create the database tables and optionally add sample data
"""

from app import app, db
from models import User, Machine, Enquiry
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_tables():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Tables created successfully!")

def add_sample_data():
    """Add sample data for testing"""
    with app.app_context():
        print("Adding sample data...")
        
        # Create sample users
        admin_user = User(
            name='Admin User',
            email='admin@b2b.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        
        supplier1 = User(
            name='Tech Machines Pvt Ltd',
            email='supplier1@techmachines.com',
            password_hash=generate_password_hash('supplier123'),
            role='supplier'
        )
        
        supplier2 = User(
            name='Industrial Solutions',
            email='supplier2@industrial.com',
            password_hash=generate_password_hash('supplier123'),
            role='supplier'
        )
        
        buyer1 = User(
            name='ABC Manufacturing',
            email='buyer1@abcmanufacturing.com',
            password_hash=generate_password_hash('buyer123'),
            role='buyer'
        )
        
        buyer2 = User(
            name='XYZ Industries',
            email='buyer2@xyzindustries.com',
            password_hash=generate_password_hash('buyer123'),
            role='buyer'
        )
        
        # Add users to database
        db.session.add_all([admin_user, supplier1, supplier2, buyer1, buyer2])
        db.session.commit()
        
        # Create sample machines
        machine1 = Machine(
            supplier_id=supplier1.id,
            name='CNC Milling Machine DMG MORI',
            category='CNC Machines',
            use_case='Precision Metal Cutting and Drilling',
            price_range='₹15,00,000 - ₹25,00,000',
            description='High-precision CNC milling machine with 3-axis control. Suitable for aerospace, automotive, and general engineering applications. Features include automatic tool changer, coolant system, and digital readout.',
            image_front='https://via.placeholder.com/600x400?text=CNC+Front+View',
            image_side='https://via.placeholder.com/600x400?text=CNC+Side+View',
            image_working='https://via.placeholder.com/600x400?text=CNC+Working',
            image_closeup='https://via.placeholder.com/600x400?text=CNC+Closeup',
            production_capacity='500-1000 units per 8-hour shift',
            automation_level='Semi-Automatic',
            power_requirement='440V, 3 Phase, 15 kW',
            machine_dimensions='12ft × 8ft × 6ft (L×W×H)',
            raw_material='Mild Steel, Stainless Steel, Aluminum',
            operator_skill='Semi-skilled technician required',
            warranty_info='1 year manufacturer warranty + service support',
            ideal_industry='Automotive, Aerospace, General Engineering',
            business_size_fit='Medium Unit (50-200 employees)',
            installation_support='yes'
        )
        
        machine2 = Machine(
            supplier_id=supplier1.id,
            name='Lathe Machine Harrison M250',
            category='Lathe Machines',
            use_case='Metal Turning and Shaping',
            price_range='₹8,00,000 - ₹12,00,000',
            description='Professional grade lathe machine perfect for small to medium-sized workshops. Features variable speed control, digital display, and high precision spindle. Ideal for batch production and custom machining.',
            image_front='https://via.placeholder.com/600x400?text=Lathe+Front+View',
            image_side='https://via.placeholder.com/600x400?text=Lathe+Side+View',
            image_working='https://via.placeholder.com/600x400?text=Lathe+Working',
            image_closeup='https://via.placeholder.com/600x400?text=Lathe+Closeup',
            production_capacity='300-600 units per 8-hour shift',
            automation_level='Manual',
            power_requirement='440V, 3 Phase, 7.5 kW',
            machine_dimensions='8ft × 4ft × 5ft (L×W×H)',
            raw_material='Mild Steel, Brass, Aluminum',
            operator_skill='Skilled operator required',
            warranty_info='2 years manufacturer warranty',
            ideal_industry='Metal Fabrication, Automotive Parts',
            business_size_fit='Small MSME (10-50 employees)',
            installation_support='yes'
        )
        
        machine3 = Machine(
            supplier_id=supplier2.id,
            name='Hydraulic Press Machine 100 Ton',
            category='Press Machines',
            use_case='Metal Forming and Stamping',
            price_range='₹6,00,000 - ₹10,00,000',
            description='Heavy-duty hydraulic press suitable for metal forming, stamping, and pressing operations. Features include pressure gauge, safety guards, and adjustable stroke length.',
            image_front='https://via.placeholder.com/600x400?text=Press+Front+View',
            image_side='https://via.placeholder.com/600x400?text=Press+Side+View',
            image_working='https://via.placeholder.com/600x400?text=Press+Working',
            image_closeup='https://via.placeholder.com/600x400?text=Press+Closeup',
            production_capacity='200-400 units per hour',
            automation_level='Semi-Automatic',
            power_requirement='440V, 3 Phase, 10 kW',
            machine_dimensions='10ft × 6ft × 8ft (L×W×H)',
            raw_material='Mild Steel, Stainless Steel',
            operator_skill='Semi-skilled technician required',
            warranty_info='1 year manufacturer warranty + on-site service',
            ideal_industry='Metal Stamping, Automotive, Appliances',
            business_size_fit='Medium Unit (50-200 employees)',
            installation_support='yes'
        )
        
        machine4 = Machine(
            supplier_id=supplier2.id,
            name='MIG Welding Machine ESAB',
            category='Welding Machines',
            use_case='Metal Fabrication and Joining',
            price_range='₹1,50,000 - ₹3,00,000',
            description='Professional MIG welding machine with advanced features. Suitable for stainless steel, aluminum, and carbon steel welding. Includes wire feeder, gas regulator, and welding torch.',
            image_front='https://via.placeholder.com/600x400?text=Welding+Front+View',
            image_side='https://via.placeholder.com/600x400?text=Welding+Side+View',
            image_working='https://via.placeholder.com/600x400?text=Welding+Working',
            image_closeup='https://via.placeholder.com/600x400?text=Welding+Closeup',
            production_capacity='Continuous operation',
            automation_level='Manual',
            power_requirement='230V, Single Phase, 5 kW',
            machine_dimensions='3ft × 2ft × 4ft (L×W×H)',
            raw_material='Mild Steel, Stainless Steel, Aluminum',
            operator_skill='Skilled welder required',
            warranty_info='6 months warranty + service support',
            ideal_industry='Metal Fabrication, Construction, Shipbuilding',
            business_size_fit='Small MSME (10-50 employees)',
            installation_support='no'
        )
        
        machine5 = Machine(
            supplier_id=supplier1.id,
            name='Laser Cutting Machine Fiber',
            category='Cutting Machines',
            use_case='Precision Metal Cutting',
            price_range='₹20,00,000 - ₹35,00,000',
            description='State-of-the-art fiber laser cutting machine for high-precision metal cutting. Features include CNC control, automatic focus adjustment, and exhaust system. Perfect for sheet metal fabrication.',
            image_front='https://via.placeholder.com/600x400?text=Laser+Front+View',
            image_side='https://via.placeholder.com/600x400?text=Laser+Side+View',
            image_working='https://via.placeholder.com/600x400?text=Laser+Working',
            image_closeup='https://via.placeholder.com/600x400?text=Laser+Closeup',
            production_capacity='1000-2000 units per 8-hour shift',
            automation_level='Fully Automatic',
            power_requirement='440V, 3 Phase, 20 kW',
            machine_dimensions='15ft × 10ft × 7ft (L×W×H)',
            raw_material='Mild Steel, Stainless Steel, Aluminum, Brass',
            operator_skill='Semi-skilled technician required',
            warranty_info='2 years comprehensive warranty + training',
            ideal_industry='Sheet Metal, Signage, Electronics',
            business_size_fit='Large Enterprise (200+ employees)',
            installation_support='yes'
        )
        
        # Add machines to database
        db.session.add_all([machine1, machine2, machine3, machine4, machine5])
        db.session.commit()
        
        # Create sample enquiries
        enquiry1 = Enquiry(
            buyer_id=buyer1.id,
            machine_id=machine1.id,
            message='We are looking for a CNC milling machine for our aerospace component manufacturing. Could you provide more technical specifications and delivery timeline?',
            budget='₹18,00,000',
            location='Pune, Maharashtra',
            production_need='Monthly production of 500 aerospace components with tight tolerances',
            status='pending'
        )
        
        enquiry2 = Enquiry(
            buyer_id=buyer2.id,
            machine_id=machine3.id,
            message='Interested in the hydraulic press for our metal stamping operations. Please provide information about maintenance requirements and warranty.',
            budget='₹7,50,000',
            location='Gurgaon, Haryana',
            production_need='Daily stamping of automotive parts, approximately 1000 units per day',
            status='responded'
        )
        
        enquiry3 = Enquiry(
            buyer_id=buyer1.id,
            machine_id=machine4.id,
            message='Need welding solution for our fabrication workshop. What accessories are included with the machine?',
            budget='₹2,50,000',
            location='Pune, Maharashtra',
            production_need='General fabrication work, including structural steel and sheet metal',
            status='pending'
        )
        
        # Add enquiries to database
        db.session.add_all([enquiry1, enquiry2, enquiry3])
        db.session.commit()
        
        print("Sample data added successfully!")
        print("\nSample Login Credentials:")
        print("Admin: admin@b2b.com / admin123")
        print("Supplier 1: supplier1@techmachines.com / supplier123")
        print("Supplier 2: supplier2@industrial.com / supplier123")
        print("Buyer 1: buyer1@abcmanufacturing.com / buyer123")
        print("Buyer 2: buyer2@xyzindustries.com / buyer123")

def reset_database():
    """Reset database by dropping all tables and recreating them"""
    with app.app_context():
        print("Resetting database...")
        db.drop_all()
        print("All tables dropped.")
        create_tables()
        print("Database reset complete!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init':
            create_tables()
        elif command == 'sample':
            add_sample_data()
        elif command == 'reset':
            reset_database()
        elif command == 'full':
            reset_database()
            add_sample_data()
        else:
            print("Usage: python init_db.py [init|sample|reset|full]")
            print("init - Create tables only")
            print("sample - Add sample data")
            print("reset - Drop and recreate tables")
            print("full - Reset database and add sample data")
    else:
        print("Usage: python init_db.py [init|sample|reset|full]")
        print("init - Create tables only")
        print("sample - Add sample data")
        print("reset - Drop and recreate tables")
        print("full - Reset database and add sample data")
