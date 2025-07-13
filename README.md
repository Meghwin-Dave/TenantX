# TenantX

A comprehensive Frappe/ERPNext application for managing multi-level companies, enterprises, and warehouses with hierarchical organizational structures.

## Overview

TenantX provides a robust framework for managing complex organizational hierarchies including enterprises, strategic business units (SBUs), factories, and liaison offices. It's designed to handle multi-tenant scenarios with ease, offering granular control over business operations and financial management.

## Features

### 🏢 **Enterprise Management**
- Multi-level enterprise hierarchy with parent-child relationships
- Enterprise type categorization
- Separate entity management
- Tax ID and contact information tracking
- Active/inactive status management

### 🎯 **Strategic Business Units (SBUs)**
- SBU creation and management within enterprises
- Business segment association
- Factory business unit linking
- Cost center integration
- SBU head assignment

### 🏭 **Factory Business Units**
- Factory categorization and capacity management
- Warehouse integration
- Factory head assignment
- Capacity tracking with UOM
- Cost center management

### 🌍 **Liaison Offices**
- International office management
- Country-based organization
- Liaison head assignment
- Contact and address management

### 📊 **Business Segments**
- Business segment categorization
- Description and documentation
- Hierarchical organization support

## DocTypes

### 1. **Enterprise**
The core organizational unit that represents a business entity.

**Key Fields:**
- Enterprise Name & Code
- Enterprise Type (link to Enterprise Type)
- Parent Enterprise (for hierarchical structure)
- Company association
- Tax ID
- Is Group / Is Separate Entity flags
- Contact & Address information

**Naming Series:** `ENT-.#####`

### 2. **Enterprise Type**
Master data for categorizing different types of enterprises.

**Key Fields:**
- Enterprise Type name
- Description

**Naming Series:** `ENTT-.#####`

### 3. **Strategic Business Unit (SBU)**
Strategic divisions within an enterprise.

**Key Fields:**
- SBU Name & Code
- Company & Enterprise association
- Factory Business Unit linking
- Business Segment association
- SBU Head (Employee)
- Cost Center
- Factory association

**Naming Series:** `SBU-.#####`

### 4. **Business Segment**
Business segment categorization for SBUs.

**Key Fields:**
- Segment Name
- Description

**Naming Series:** `BS-.#####`

### 5. **Factory Business Unit**
Physical manufacturing or operational units.

**Key Fields:**
- Factory Name & Code
- Company & Enterprise association
- SBU linking
- Factory Category
- Capacity & Capacity UOM
- Warehouse association
- Factory Head (Employee)
- Cost Center
- Contact & Address information

**Naming Series:** `FBU-.#####`

### 6. **Factory Category**
Master data for categorizing different types of factories.

**Key Fields:**
- Factory Category name
- Description

**Naming Series:** `FC-.#####`

### 7. **Liaison Office**
International or regional representative offices.

**Key Fields:**
- Office Name & Code
- Enterprise association
- Country
- Liaison Head (Employee)
- Contact & Address information

**Naming Series:** `LO-.#####`

## Installation

### Prerequisites
- Frappe Framework (v14+)
- ERPNext (recommended)
- Bench CLI

### Installation Steps

1. **Clone the repository:**
```bash
cd $PATH_TO_YOUR_BENCH
bench get-app tenantx --branch develop
```

2. **Install the app:**
```bash
bench install-app tenantx
```

3. **Migrate the database:**
```bash
bench migrate
```

## Usage

### Setting Up Your Organization

1. **Create Enterprise Types**
   - Navigate to TenantX > Enterprise Type
   - Create types like "Manufacturing", "Trading", "Service", etc.

2. **Create Business Segments**
   - Navigate to TenantX > Business Segment
   - Create segments like "Electronics", "Automotive", "Healthcare", etc.

3. **Create Factory Categories**
   - Navigate to TenantX > Factory Category
   - Create categories like "Assembly", "Processing", "Packaging", etc.

4. **Create Enterprises**
   - Navigate to TenantX > Enterprise
   - Create your main enterprise with appropriate type
   - Set up parent-child relationships for complex hierarchies

5. **Create Strategic Business Units**
   - Navigate to TenantX > Strategic Business Unit
   - Associate with enterprises and business segments
   - Assign SBU heads and cost centers

6. **Create Factory Business Units**
   - Navigate to TenantX > Factory Business Unit
   - Link to enterprises, SBUs, and warehouses
   - Set capacity and assign factory heads

7. **Create Liaison Offices**
   - Navigate to TenantX > Liaison Office
   - Set up international offices with country information

### Hierarchical Structure Example

```
Enterprise (Parent)
├── Enterprise Type: Manufacturing
├── Strategic Business Unit 1
│   ├── Business Segment: Electronics
│   └── Factory Business Unit 1
│       ├── Factory Category: Assembly
│       └── Warehouse: Main Warehouse
├── Strategic Business Unit 2
│   ├── Business Segment: Automotive
│   └── Factory Business Unit 2
│       ├── Factory Category: Processing
│       └── Warehouse: Secondary Warehouse
└── Liaison Office
    └── Country: United States
```

## Configuration

### Permissions
All doctypes are configured with System Manager permissions by default. You can customize permissions based on your organizational needs.

### Naming Series
Each doctype uses configurable naming series for easy identification:
- Enterprise: `ENT-.#####`
- Enterprise Type: `ENTT-.#####`
- SBU: `SBU-.#####`
- Business Segment: `BS-.#####`
- Factory Business Unit: `FBU-.#####`
- Factory Category: `FC-.#####`
- Liaison Office: `LO-.#####`

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/tenantx
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

## Development

### Code Quality
- Python code follows PEP 8 standards
- JavaScript code follows ESLint configuration
- All code is automatically formatted using pre-commit hooks

### Testing
Each doctype includes basic test files. Run tests using:
```bash
bench run-tests --app tenantx
```

## License

MIT License - see [license.txt](license.txt) for details.

## Support

For support and questions:
- Email: meghwin@cognitionx.tech
- Publisher: CognitionXLogic

## Version History

- **v1.0.0**: Initial release with core organizational management features
  - Enterprise hierarchy management
  - SBU and Factory Business Unit support
  - Liaison office management
  - Business segment categorization
  - Factory category management

---

**TenantX** - Manage multi-level companies and warehouses with super ease
