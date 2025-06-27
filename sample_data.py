# Enhanced Sample Data for Sales Order Management System
from datetime import datetime, timedelta
import random

# 25 Realistic Customers
customers = [
    {"id": 1, "company_name": "Acme Corporation", "contact_person": "John Doe", "email": "john@acme.com", "phone": "555-1234", "billing_address": "123 Main St, Anytown, USA"},
    {"id": 2, "company_name": "Globex Industries", "contact_person": "Jane Smith", "email": "jane@globex.com", "phone": "555-5678", "billing_address": "456 Oak Ave, Somewhere, USA"},
    {"id": 3, "company_name": "TechFlow Solutions", "contact_person": "Mike Johnson", "email": "mike@techflow.com", "phone": "555-2468", "billing_address": "789 Pine Rd, Tech City, CA"},
    {"id": 4, "company_name": "Digital Dynamics", "contact_person": "Sarah Wilson", "email": "sarah@digitaldynamics.com", "phone": "555-1357", "billing_address": "321 Cedar Blvd, Innovation Park, TX"},
    {"id": 5, "company_name": "CloudVantage Inc", "contact_person": "David Brown", "email": "david@cloudvantage.com", "phone": "555-9753", "billing_address": "654 Elm Street, Cloud Valley, WA"},
    {"id": 6, "company_name": "NextGen Systems", "contact_person": "Lisa Garcia", "email": "lisa@nextgen.com", "phone": "555-8642", "billing_address": "987 Maple Drive, Future City, NY"},
    {"id": 7, "company_name": "InnoTech Corp", "contact_person": "Robert Miller", "email": "robert@innotech.com", "phone": "555-7531", "billing_address": "147 Birch Lane, Innovation Hub, FL"},
    {"id": 8, "company_name": "DataStream Ltd", "contact_person": "Emily Davis", "email": "emily@datastream.com", "phone": "555-4628", "billing_address": "258 Willow Ave, Data Center, CO"},
    {"id": 9, "company_name": "SmartLogic Solutions", "contact_person": "Chris Anderson", "email": "chris@smartlogic.com", "phone": "555-3697", "billing_address": "369 Spruce Way, Logic City, OR"},
    {"id": 10, "company_name": "FutureTech Enterprises", "contact_person": "Amanda Taylor", "email": "amanda@futuretech.com", "phone": "555-1472", "billing_address": "741 Aspen Court, Tomorrow Town, AZ"},
    {"id": 11, "company_name": "CyberCore Industries", "contact_person": "James Thomas", "email": "james@cybercore.com", "phone": "555-5829", "billing_address": "852 Oak Ridge, Cyber Valley, NV"},
    {"id": 12, "company_name": "Quantum Systems", "contact_person": "Michelle Lee", "email": "michelle@quantum.com", "phone": "555-9374", "billing_address": "963 Quantum Lane, Physics Park, MA"},
    {"id": 13, "company_name": "ByteWorks Inc", "contact_person": "Kevin White", "email": "kevin@byteworks.com", "phone": "555-6185", "billing_address": "159 Binary Boulevard, Code City, UT"},
    {"id": 14, "company_name": "AlgoLogic Corp", "contact_person": "Rachel Green", "email": "rachel@algologic.com", "phone": "555-2749", "billing_address": "357 Algorithm Ave, Logic Land, ID"},
    {"id": 15, "company_name": "DevStream Technologies", "contact_person": "Mark Robinson", "email": "mark@devstream.com", "phone": "555-4816", "billing_address": "468 Developer Drive, Code Valley, MT"},
    {"id": 16, "company_name": "CloudBridge Solutions", "contact_person": "Nicole Clark", "email": "nicole@cloudbridge.com", "phone": "555-7392", "billing_address": "579 Bridge Street, Cloud City, WY"},
    {"id": 17, "company_name": "TechMerge Inc", "contact_person": "Brian Hall", "email": "brian@techmerge.com", "phone": "555-5274", "billing_address": "681 Merge Road, Tech Town, VT"},
    {"id": 18, "company_name": "DataFlow Dynamics", "contact_person": "Jessica Adams", "email": "jessica@dataflow.com", "phone": "555-8516", "billing_address": "792 Flow Avenue, Data District, NH"},
    {"id": 19, "company_name": "CodeCraft Studios", "contact_person": "Andrew Baker", "email": "andrew@codecraft.com", "phone": "555-3947", "billing_address": "813 Craft Circle, Studio City, ME"},
    {"id": 20, "company_name": "NetWork Solutions", "contact_person": "Stephanie King", "email": "stephanie@network.com", "phone": "555-7158", "billing_address": "924 Network Plaza, Connection City, DE"},
    {"id": 21, "company_name": "PixelPerfect Design", "contact_person": "Daniel Scott", "email": "daniel@pixelperfect.com", "phone": "555-6283", "billing_address": "135 Pixel Lane, Design District, RI"},
    {"id": 22, "company_name": "SystemCore Tech", "contact_person": "Ashley Turner", "email": "ashley@systemcore.com", "phone": "555-4729", "billing_address": "246 Core Street, System City, CT"},
    {"id": 23, "company_name": "LogicBridge Corp", "contact_person": "Ryan Phillips", "email": "ryan@logicbridge.com", "phone": "555-8364", "billing_address": "357 Logic Way, Bridge Town, HI"},
    {"id": 24, "company_name": "DataVault Security", "contact_person": "Lauren Campbell", "email": "lauren@datavault.com", "phone": "555-1597", "billing_address": "468 Vault Road, Security City, AK"},
    {"id": 25, "company_name": "CloudNet Innovations", "contact_person": "Tyler Evans", "email": "tyler@cloudnet.com", "phone": "555-7241", "billing_address": "579 Innovation Blvd, Cloud Center, ND"}
]

# 30 Diverse Products
products = [
    {"id": 1, "sku": "PROD-001", "product_name": "Deluxe Widget", "description": "A premium quality widget for enterprise applications", "unit_price": 29.99, "inventory_quantity": 100},
    {"id": 2, "sku": "PROD-002", "product_name": "Super Gadget", "description": "The latest in gadget technology with AI integration", "unit_price": 49.99, "inventory_quantity": 50},
    {"id": 3, "sku": "CLOUD-001", "product_name": "CloudSync Pro", "description": "Professional cloud synchronization software license", "unit_price": 199.99, "inventory_quantity": 75},
    {"id": 4, "sku": "SEC-001", "product_name": "SecureVault Enterprise", "description": "Advanced security solution for business data protection", "unit_price": 299.99, "inventory_quantity": 40},
    {"id": 5, "sku": "DEV-001", "product_name": "DevTools Master Suite", "description": "Complete development toolkit for software engineers", "unit_price": 149.99, "inventory_quantity": 60},
    {"id": 6, "sku": "DATA-001", "product_name": "DataAnalyzer Pro", "description": "Professional data analysis and visualization platform", "unit_price": 249.99, "inventory_quantity": 35},
    {"id": 7, "sku": "MOBILE-001", "product_name": "MobileApp Builder", "description": "No-code mobile application development platform", "unit_price": 179.99, "inventory_quantity": 45},
    {"id": 8, "sku": "WEB-001", "product_name": "WebDesign Studio", "description": "Professional web design and development suite", "unit_price": 129.99, "inventory_quantity": 80},
    {"id": 9, "sku": "API-001", "product_name": "API Gateway Enterprise", "description": "Advanced API management and gateway solution", "unit_price": 399.99, "inventory_quantity": 25},
    {"id": 10, "sku": "DB-001", "product_name": "DatabasePro Manager", "description": "Professional database management and optimization tool", "unit_price": 219.99, "inventory_quantity": 55},
    {"id": 11, "sku": "BACKUP-001", "product_name": "BackupMaster Pro", "description": "Automated backup and recovery solution", "unit_price": 99.99, "inventory_quantity": 90},
    {"id": 12, "sku": "MONITOR-001", "product_name": "SystemMonitor Elite", "description": "Real-time system monitoring and alerting platform", "unit_price": 159.99, "inventory_quantity": 70},
    {"id": 13, "sku": "CRM-001", "product_name": "CRM Connect Pro", "description": "Customer relationship management software", "unit_price": 189.99, "inventory_quantity": 65},
    {"id": 14, "sku": "ERP-001", "product_name": "ERP Solutions Suite", "description": "Enterprise resource planning system", "unit_price": 499.99, "inventory_quantity": 20},
    {"id": 15, "sku": "PROJ-001", "product_name": "ProjectManager Pro", "description": "Advanced project management and collaboration tool", "unit_price": 139.99, "inventory_quantity": 85},
    {"id": 16, "sku": "COMM-001", "product_name": "TeamComm Enterprise", "description": "Business communication and messaging platform", "unit_price": 79.99, "inventory_quantity": 120},
    {"id": 17, "sku": "DOC-001", "product_name": "DocumentFlow Pro", "description": "Document management and workflow automation", "unit_price": 119.99, "inventory_quantity": 95},
    {"id": 18, "sku": "ANAL-001", "product_name": "Analytics Dashboard", "description": "Business intelligence and analytics platform", "unit_price": 279.99, "inventory_quantity": 30},
    {"id": 19, "sku": "INTEG-001", "product_name": "Integration Hub", "description": "Enterprise application integration platform", "unit_price": 349.99, "inventory_quantity": 40},
    {"id": 20, "sku": "AI-001", "product_name": "AI Assistant Pro", "description": "Artificial intelligence productivity assistant", "unit_price": 229.99, "inventory_quantity": 50},
    {"id": 21, "sku": "BLOCK-001", "product_name": "Blockchain Validator", "description": "Blockchain transaction validation service", "unit_price": 459.99, "inventory_quantity": 15},
    {"id": 22, "sku": "IOT-001", "product_name": "IoT Connect Platform", "description": "Internet of Things device management platform", "unit_price": 319.99, "inventory_quantity": 35},
    {"id": 23, "sku": "VR-001", "product_name": "VR Meeting Space", "description": "Virtual reality collaboration environment", "unit_price": 199.99, "inventory_quantity": 25},
    {"id": 24, "sku": "GAME-001", "product_name": "GameDev Engine Pro", "description": "Professional game development engine license", "unit_price": 169.99, "inventory_quantity": 45},
    {"id": 25, "sku": "VOICE-001", "product_name": "VoiceAI Assistant", "description": "Voice-activated AI business assistant", "unit_price": 189.99, "inventory_quantity": 60},
    {"id": 26, "sku": "COMP-001", "product_name": "CloudCompute Credits", "description": "High-performance cloud computing credits", "unit_price": 0.15, "inventory_quantity": 10000},
    {"id": 27, "sku": "STORE-001", "product_name": "DataStorage Premium", "description": "Premium cloud storage solution per GB", "unit_price": 0.08, "inventory_quantity": 50000},
    {"id": 28, "sku": "BAND-001", "product_name": "Bandwidth Pro Package", "description": "High-speed bandwidth allocation per TB", "unit_price": 25.99, "inventory_quantity": 500},
    {"id": 29, "sku": "SUPP-001", "product_name": "Premium Support Plan", "description": "24/7 premium technical support package", "unit_price": 299.99, "inventory_quantity": 100},
    {"id": 30, "sku": "TRAIN-001", "product_name": "Training Workshop", "description": "Professional software training and certification", "unit_price": 399.99, "inventory_quantity": 30}
]

# Generate 40 realistic orders with proper line items
def generate_orders():
    orders = []
    base_date = datetime.now() - timedelta(days=90)  # Start 90 days ago
    
    statuses = ['unissued', 'issued', 'complete', 'voided']
    payment_statuses = ['unpaid', 'partial', 'paid']
    
    for i in range(1, 41):  # 40 orders
        # Random customer and date
        customer_id = random.randint(1, 25)
        customer = next(c for c in customers if c['id'] == customer_id)
        order_date = base_date + timedelta(days=random.randint(0, 89))
        
        # Generate 1-5 line items per order
        line_items = []
        num_items = random.randint(1, 5)
        total_amount = 0
        
        for j in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            unit_price = product['unit_price']
            line_total = quantity * unit_price
            total_amount += line_total
            
            line_item = {
                "id": j + 1,
                "product_id": product['id'],
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
                "fulfillment_status": random.choice(['unfulfilled', 'partially_fulfilled', 'fulfilled'])
            }
            line_items.append(line_item)
        
        # Determine status based on order age
        days_old = (datetime.now() - order_date).days
        if days_old < 10:
            status = random.choice(['unissued', 'issued'])
            payment_status = 'unpaid'
        elif days_old < 30:
            status = random.choice(['issued', 'complete'])
            payment_status = random.choice(['unpaid', 'partial', 'paid'])
        else:
            status = random.choice(['complete', 'voided'])
            payment_status = 'paid' if status == 'complete' else 'unpaid'
        
        order = {
            "id": i,
            "order_number": f"ORD-{order_date.strftime('%Y%m%d')}-{i:03d}",
            "customer_id": customer_id,
            "customer": customer,
            "order_date": order_date.isoformat(),
            "status": status,
            "payment_status": payment_status,
            "total_amount": round(total_amount, 2),
            "delivery_address": f"{customer['billing_address']} (Delivery)",
            "line_items": line_items
        }
        orders.append(order)
    
    return orders

# Generate the orders
orders = generate_orders()

# Summary statistics
print(f"Generated sample data:")
print(f"- {len(customers)} customers")
print(f"- {len(products)} products") 
print(f"- {len(orders)} orders")
print(f"- Total revenue: ${sum(o['total_amount'] for o in orders if o['status'] == 'complete'):,.2f}")
