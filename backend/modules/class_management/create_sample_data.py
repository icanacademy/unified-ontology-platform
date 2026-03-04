import sqlite3
from datetime import datetime

def create_sample_data():
    conn = sqlite3.connect('ican_classes.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS class_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR UNIQUE,
            description TEXT,
            color VARCHAR DEFAULT '#1976d2'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            description TEXT,
            category_id INTEGER,
            min_grade_level VARCHAR,
            max_grade_level VARCHAR,
            difficulty_level INTEGER,
            duration_weeks INTEGER,
            skills_focus TEXT,
            learning_objectives TEXT,
            materials_needed TEXT,
            assessment_methods TEXT,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES class_categories (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            email VARCHAR UNIQUE,
            current_grade_level VARCHAR,
            english_proficiency_level VARCHAR,
            join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            class_id INTEGER,
            enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            completion_date DATETIME,
            progress_percentage REAL DEFAULT 0.0,
            current_level VARCHAR,
            performance_score REAL,
            teacher_notes TEXT,
            is_completed BOOLEAN DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            description TEXT,
            target_grade_level VARCHAR,
            target_proficiency VARCHAR,
            estimated_duration_months INTEGER,
            class_sequence TEXT,
            is_recommended BOOLEAN DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS class_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            teacher_name VARCHAR,
            day_of_week VARCHAR,
            start_time VARCHAR,
            end_time VARCHAR,
            classroom VARCHAR,
            max_students INTEGER DEFAULT 12,
            current_enrolled INTEGER DEFAULT 0,
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')
    
    # Insert categories
    categories = [
        ("Reading Track", "Reading comprehension and vocabulary development", "#2196F3"),
        ("Writing Track", "Writing skills from basic to advanced", "#4CAF50"),
        ("Speaking Track", "Oral communication and presentation skills", "#FF9800"),
        ("Test Preparation", "Standardized test preparation courses", "#9C27B0"),
        ("Advanced Courses", "High-level academic preparation", "#F44336"),
        ("STEM Integration", "Science, Technology, Engineering, Math with ESL", "#607D8B")
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO class_categories (name, description, color) VALUES (?, ?, ?)', categories)
    
    # Insert ICAN classes
    classes_data = [
        # Reading Track
        ("Book Club", "Select books appropriate for reading level with pronunciation corrections and storytelling training", 1, "G1", "G6", 2, 8, "Reading, Pronunciation, Storytelling", "Improve reading fluency and narrative skills", "Chapter books, series books", "Reading assessments, story retelling", 1),
        ("Reading and Vocabulary", "Non-fiction topics in science and society with vocabulary building", 1, "G2", "G6", 3, 10, "Reading comprehension, Vocabulary, Background knowledge", "Build reading skills and expand vocabulary", "Non-fiction texts, media resources", "Vocabulary tests, comprehension quizzes", 1),
        ("Reading to Writing", "Detailed story reading with summary writing using American textbooks", 1, "G3", "G6", 4, 12, "Reading analysis, Summary writing, Critical thinking", "Develop deep reading comprehension and writing skills", "Houghton textbooks, American curriculum materials", "Written summaries, analysis papers", 1),
        
        # Writing Track
        ("Comprehensive Writing (G1-G3)", "Basic sentence structures and patterns for writing beginners", 2, "G1", "G3", 1, 10, "Basic grammar, Sentence structure, Descriptive writing", "Overcome fear of English writing", "Grammar workbooks, writing prompts", "Writing portfolios, peer reviews", 1),
        ("Creative Writing 1 (G2-G4)", "Short story creation with illustrations and teacher guidance", 2, "G2", "G4", 2, 8, "Creative storytelling, Illustration, Self-expression", "Develop creativity and storytelling skills", "Picture prompts, art supplies", "Story collections, creative projects", 1),
        ("Creative Writing 2", "Long-form writing in various genres with character development", 2, "G4", "G6", 4, 12, "Genre writing, Character development, Advanced vocabulary", "Master various writing genres", "Genre examples, advanced vocabulary lists", "Published student books, genre portfolios", 1),
        ("Grammar to Writing (G4-G6)", "Four paragraph types with idioms and complex sentences", 2, "G4", "G6", 3, 10, "Paragraph structure, Grammar application, Sentence variety", "Write systematically and logically", "Grammar guides, writing frameworks", "Paragraph assessments, grammar tests", 1),
        ("Essay Clinic (G6+)", "Advanced essay editing and in-depth organized writing", 2, "G6", "High School", 5, 8, "Essay structure, Advanced grammar, Critical analysis", "Complete independent essay writing", "Essay examples, editing guides", "Completed essays, peer editing", 1),
        
        # Speaking Track
        ("Creative Sparks", "Five senses exploration with songs, games, and picture books", 3, "Preschool", "G2", 1, 6, "Sensory learning, Basic vocabulary, Speaking confidence", "Open up language learning through senses", "Songs, games, picture books, art materials", "Oral presentations, participation assessment", 1),
        ("Speech Power", "Creative storytelling, monologues, and presentation skills", 3, "G3", "G6", 3, 10, "Public speaking, Creative presentation, Confidence building", "Develop presentation skills and overcome speaking fear", "Speech topics, presentation tools", "Weekly presentations, confidence assessments", 1),
        ("TED Class", "TED video analysis with PPT presentations and Q&A sessions", 3, "G5", "High School", 5, 12, "Advanced presentation, Critical analysis, Public speaking", "Professional presentation skills", "TED videos, presentation software", "TED-style presentations, audience evaluations", 1),
        
        # Test Preparation
        ("TOEFL", "Four major areas with academic English and background knowledge", 4, "G6", "High School", 5, 16, "Academic English, Test strategies, Critical thinking", "Achieve high TOEFL scores", "TOEFL materials, Cornell notebooks", "Mock tests, skill assessments", 1),
        ("SAT", "Literacy, numeracy, and writing skills for US university admission", 4, "High School", "High School", 5, 20, "Critical reading, Mathematical reasoning, Essay writing", "Prepare for US university admission", "SAT prep books, diagnostic tests", "Practice SATs, progress tracking", 1),
        ("IELTS", "Four skills assessment for English-speaking countries", 4, "G6", "High School", 4, 12, "Listening, Reading, Writing, Speaking", "Achieve target IELTS band scores", "IELTS practice materials, simulation tests", "Mock IELTS tests, band score tracking", 1),
        
        # Advanced Courses
        ("SAT Book Bridge", "Literature and classic novels with deep analytical skills", 5, "High School", "High School", 5, 16, "Literary analysis, Critical thinking, Advanced inference", "Develop high-level literary skills", "Classic literature, analysis guides", "Literary critiques, analytical essays", 1),
        ("News Clipping", "Current affairs discussion with article analysis and debate", 5, "G5", "High School", 4, 8, "Current events, Critical discussion, Analytical writing", "Develop critical thinking and social awareness", "News articles, discussion topics", "Article summaries, debate assessments", 1),
        ("AP Classes", "College-level academic experience with advanced credits", 5, "High School", "High School", 5, 18, "College-level academics, Critical analysis, Advanced problem-solving", "Earn college credits and develop academic skills", "AP textbooks, college-level materials", "AP exams, college-level assessments", 1),
        
        # STEM Integration
        ("EduSpace", "Space-related integrated program with hands-on problem solving", 6, "G4", "G5", 3, 8, "STEM integration, Problem-solving, Research skills", "Develop inquiry and technology skills", "Space materials, technology tools", "Project presentations, collaborative assessments", 1),
        ("Coding", "Logical thinking and problem-solving through programming", 6, "G3", "High School", 3, 12, "Programming logic, Problem-solving, Technical thinking", "Develop coding skills and logical thinking", "Programming tools, development environments", "Coding projects, technical assessments", 1)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO classes (name, description, category_id, min_grade_level, max_grade_level, difficulty_level, duration_weeks, skills_focus, learning_objectives, materials_needed, assessment_methods, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', classes_data)
    
    # Insert sample students
    students_data = [
        ("Emma Johnson", "emma.johnson@email.com", "G3", "Intermediate", "Active student with strong reading interests"),
        ("Carlos Rodriguez", "carlos.rodriguez@email.com", "G5", "Advanced", "Excellent in speaking, needs writing support"),
        ("Yuki Tanaka", "yuki.tanaka@email.com", "G2", "Beginner", "New ESL student, very motivated"),
        ("Sofia Chen", "sofia.chen@email.com", "G4", "Intermediate", "Strong in writing, working on speaking confidence"),
        ("Ahmed Hassan", "ahmed.hassan@email.com", "High School", "Advanced", "Preparing for university entrance exams"),
        ("Maria Gonzales", "maria.gonzales@email.com", "G1", "Beginner", "Young learner, enjoys creative activities"),
        ("David Kim", "david.kim@email.com", "G6", "Advanced", "Excellent all-around student, ready for challenges"),
        ("Ana Silva", "ana.silva@email.com", "G3", "Intermediate", "Loves reading, needs grammar support")
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO students (name, email, current_grade_level, english_proficiency_level, notes) VALUES (?, ?, ?, ?, ?)', students_data)
    
    # Insert sample learning paths
    learning_paths_data = [
        ("Beginning Reader Path", "For new ESL students starting their reading journey", "G1", "Beginner", 6, "[1, 4, 9]", 1),
        ("Advanced Writing Path", "For students ready to master academic writing", "G4", "Advanced", 8, "[7, 8, 16]", 1),
        ("Speaking Confidence Path", "Build speaking skills from basic to presentation level", "G3", "Intermediate", 7, "[9, 10, 11]", 1),
        ("Test Prep Intensive", "Comprehensive preparation for standardized tests", "High School", "Advanced", 12, "[12, 13, 14]", 1),
        ("Creative Expression Path", "For students who love creative writing and storytelling", "G2", "Intermediate", 5, "[1, 5, 6]", 1)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO learning_paths (name, description, target_grade_level, target_proficiency, estimated_duration_months, class_sequence, is_recommended) VALUES (?, ?, ?, ?, ?, ?, ?)', learning_paths_data)
    
    # Insert sample progress records
    progress_data = [
        (1, 1, "2024-01-15 10:00:00", None, 75.0, "Intermediate", 85.0, "Excellent progress in storytelling", 0),
        (1, 4, "2024-01-15 10:00:00", "2024-03-15 10:00:00", 100.0, "Advanced", 92.0, "Completed with outstanding results", 1),
        (2, 10, "2024-02-01 09:00:00", None, 60.0, "Advanced", 88.0, "Great speaking skills, confidence building", 0),
        (3, 9, "2024-02-15 11:00:00", None, 40.0, "Beginner", 78.0, "Good progress for new student", 0),
        (4, 7, "2024-01-20 14:00:00", None, 85.0, "Intermediate", 90.0, "Strong grammar understanding", 0),
        (5, 12, "2024-01-10 15:00:00", None, 70.0, "Advanced", 85.0, "Preparing well for TOEFL", 0)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO student_progress (student_id, class_id, enrollment_date, completion_date, progress_percentage, current_level, performance_score, teacher_notes, is_completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', progress_data)
    
    # Insert sample schedules
    schedule_data = [
        (1, "Ms. Sarah Thompson", "Monday", "09:00", "10:30", "Room A1", 8, 5),
        (1, "Ms. Sarah Thompson", "Wednesday", "09:00", "10:30", "Room A1", 8, 5),
        (4, "Mr. David Park", "Tuesday", "14:00", "15:30", "Room B2", 10, 8),
        (4, "Mr. David Park", "Thursday", "14:00", "15:30", "Room B2", 10, 8),
        (10, "Ms. Jennifer Lee", "Friday", "10:00", "11:30", "Room C3", 12, 10),
        (11, "Dr. Michael Chen", "Monday", "16:00", "17:30", "Room D4", 15, 12),
        (12, "Ms. Lisa Wang", "Saturday", "09:00", "12:00", "Room E5", 20, 18)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO class_schedules (class_id, teacher_name, day_of_week, start_time, end_time, classroom, max_students, current_enrolled) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', schedule_data)
    
    conn.commit()
    conn.close()
    print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()