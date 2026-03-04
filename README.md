# 🎓 Unified Ontology Platform

**Integrated Educational Analytics Platform**

A comprehensive unified system that consolidates all educational analytics platforms into a single, cohesive web application accessible through one IP address and port.

## 🌟 Overview

This unified platform integrates five distinct educational analytics systems:

- **📚 Books & Library Management** - Comprehensive library management with AI-powered features
- **👨‍🏫 Faculty Analytics** - Faculty performance and research analytics platform  
- **🎓 Student Analytics** - Student performance tracking and analytics
- **📋 Class Management** - ESL curriculum and class management system
- **🧠 Ontology Platform** - Advanced ontology management and analysis

## 🚀 Key Features

- **Single Access Point**: All platforms accessible through `http://localhost:8000`
- **Unified Navigation**: Seamless switching between platforms
- **Preserved Functionality**: All original platform features maintained
- **Modular Architecture**: Each platform remains independent internally
- **Database Independence**: Each platform maintains its own database schema
- **Integrated API**: Comprehensive REST API with interactive documentation

## 📁 Project Structure

```
unified-ontology-platform/
├── backend/
│   ├── main.py                    # Main unified FastAPI application
│   ├── database.py               # Unified database configuration
│   ├── requirements.txt          # Python dependencies
│   ├── modules/                  # Modular platform backends
│   │   ├── books/               # Books platform module
│   │   ├── faculty/             # Faculty analytics module
│   │   ├── student/             # Student analytics module
│   │   ├── class_management/    # Class management module
│   │   └── ontology/            # Ontology platform module
│   └── databases/               # All database files
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main React application
│   │   ├── components/
│   │   │   ├── Navigation.tsx   # Unified navigation
│   │   │   ├── Dashboard.tsx    # Main dashboard
│   │   │   └── platforms/       # Platform-specific components
│   │   └── services/
│   │       └── api.ts           # Unified API service
└── scripts/
    ├── setup.py                 # Installation script
    └── start.py                 # Unified startup script
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (optional, for frontend)
- npm/yarn (optional, for frontend)

### Quick Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd "/Users/icanacademy/unified-ontology-platform"
   ```

2. **Run the setup script:**
   ```bash
   python3 scripts/setup.py
   ```

3. **Start the unified platform:**
   ```bash
   python3 scripts/start.py
   ```

### Manual Setup

If you prefer manual setup:

1. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Install frontend dependencies (optional):**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the backend:**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Start the frontend (optional):**
   ```bash
   cd frontend
   npm start
   ```

## 🔗 Access Points

Once running, access the platform at:

### Main Access
- **🏠 Main Dashboard**: http://localhost:8000
- **📖 API Documentation**: http://localhost:8000/api/docs
- **🎨 Frontend** (if running): http://localhost:3000

### Platform Endpoints
- **📚 Books & Library**: http://localhost:8000/api/books
- **👨‍🏫 Faculty Analytics**: http://localhost:8000/api/faculty  
- **🎓 Student Analytics**: http://localhost:8000/api/students
- **📋 Class Management**: http://localhost:8000/api/classes
- **🧠 Ontology Platform**: http://localhost:8000/api/ontology

## 📊 Platform Details

### Books & Library Management
- Book catalog management
- User management and circulation
- Checkout/return system
- AI-powered recommendations
- Library analytics and reporting

### Faculty Analytics
- Faculty performance tracking
- Research metrics analysis
- Teaching effectiveness evaluation
- Professional development tracking
- AI-powered insights and recommendations

### Student Analytics  
- Student performance monitoring
- Assessment analytics
- Learning progress tracking
- At-risk student identification
- Teaching strategy recommendations

### Class Management
- ESL curriculum management
- Class scheduling and organization
- Student progress tracking
- Learning path recommendations
- Course difficulty analysis

### Ontology Platform
- Knowledge graph construction
- Semantic analysis and querying
- Educational data integration
- Advanced ontology management
- Cross-platform data relationships

## 🗄️ Database Architecture

Each platform maintains its own SQLite database:
- `books_library.db` - Books & Library data
- `faculty_analytics.db` - Faculty data and metrics
- `student_analytics.db` - Student performance data
- `ican_classes.db` - Class management data
- `ontology_platform.db` - Ontology and knowledge data

Databases are automatically created and managed by the system.

## 🎯 Usage

1. **Access the main dashboard** at http://localhost:8000
2. **Navigate between platforms** using the unified navigation bar
3. **Use platform-specific features** by clicking on platform cards
4. **Access API endpoints** directly or via the interactive documentation
5. **Switch seamlessly** between different educational analytics tools

## 🔧 Development

### Adding New Features
- Backend features: Add to respective module in `backend/modules/`
- Frontend features: Add to respective platform in `frontend/src/components/platforms/`
- Database changes: Modify platform-specific database configurations

### API Development
- Each platform maintains its own router in `modules/{platform}/router.py`
- All routes are automatically prefixed with `/api/{platform}`
- Interactive API documentation available at `/api/docs`

## 🚀 Deployment

For production deployment:

1. **Set environment variables:**
   ```bash
   export REACT_APP_API_URL=https://your-domain.com
   ```

2. **Build frontend:**
   ```bash
   cd frontend
   npm run build
   ```

3. **Run with production server:**
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

## 📈 Benefits

- **Unified Access**: Single entry point for all educational analytics
- **Seamless Integration**: Easy navigation between different platforms
- **Preserved Functionality**: All original features maintained
- **Scalable Architecture**: Easy to add new platforms or features
- **Consistent Experience**: Unified UI/UX across all platforms
- **Efficient Resource Usage**: Shared infrastructure and dependencies

## 🤝 Support

For issues or questions:
1. Check the API documentation at http://localhost:8000/api/docs
2. Verify all services are running with `python3 scripts/start.py`
3. Check database files in `backend/databases/`

## 📝 Version

**Version 1.0.0** - Initial unified platform release

---

**🎓 Unified Ontology Platform - Bringing all educational analytics together in one comprehensive system.**