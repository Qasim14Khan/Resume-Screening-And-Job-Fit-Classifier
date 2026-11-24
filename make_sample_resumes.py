"""Generate 12 realistic, FICTIONAL sample resumes (PDF) into sample_resumes/.
File names carry the true field (e.g. Data_Science_1.pdf) so Demo mode can check the model.
Run:  python make_sample_resumes.py      (needs: pip install reportlab)"""
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

R = {}
R["Data_Science_1"] = dict(name="Ayesha Siddiqui", title="Data Scientist", city="Karachi, Pakistan",
 summary="Data scientist with 4 years of experience building machine learning models for churn, demand forecasting and customer segmentation. Strong in Python, statistics and communicating results to business teams.",
 skills="Python, Pandas, NumPy, Scikit-learn, TensorFlow, Keras, SQL, Tableau, Statistics, Machine Learning, Deep Learning, Data Visualization, Feature Engineering, A/B Testing, Git",
 jobs=[("Data Scientist", "Telenor Analytics, Karachi", "2022 - Present", ["Built a churn prediction model with gradient boosting and scikit-learn that raised retention campaign precision by 18%.", "Cleaned and analysed 3 million customer records using Pandas and SQL; automated weekly reports.", "Designed A/B tests and presented statistical results to the marketing team using Tableau dashboards."]),
       ("Junior Data Analyst", "DataBridge Solutions, Karachi", "2020 - 2022", ["Created regression and classification models in Python for sales forecasting.", "Built data visualization dashboards and trained 10 colleagues on SQL and Pandas."])],
 edu=["BS Computer Science, NED University of Engineering and Technology, 2020"],
 projects=["Image classifier using TensorFlow and Keras (CNN) reaching 94% accuracy on a public dataset.", "Customer segmentation with K-Means clustering and PCA on retail transaction data."])
R["Data_Science_2"] = dict(name="Hamza Ali Khan", title="Machine Learning Engineer", city="Lahore, Pakistan",
 summary="Machine learning engineer focused on natural language processing and predictive modelling. Experienced in taking models from notebooks to production APIs.",
 skills="Python, Machine Learning, NLP, Deep Learning, PyTorch, TensorFlow, Scikit-learn, Pandas, NumPy, SQL, Statistics, Data Mining, Docker, Flask, Jupyter",
 jobs=[("Machine Learning Engineer", "Arbisoft, Lahore", "2021 - Present", ["Developed a text classification model with TF-IDF and logistic regression for support ticket routing.", "Trained deep learning models in PyTorch for sentiment analysis; deployed with Flask and Docker.", "Performed exploratory data analysis, feature engineering and model evaluation with cross-validation."]),
       ("Data Analyst Intern", "Systems Limited, Lahore", "2020 - 2021", ["Wrote SQL queries and Python scripts for data cleaning and statistical analysis."])],
 edu=["MS Data Science, FAST National University, 2022", "BS Software Engineering, UET Lahore, 2020"],
 projects=["Resume parser using NLP and named entity recognition.", "Time series forecasting of electricity demand with LSTM networks."])
R["Java_Developer_1"] = dict(name="Bilal Ahmed", title="Java Developer", city="Islamabad, Pakistan",
 summary="Java developer with 5 years of experience building enterprise web applications and REST services with Spring Boot and Hibernate.",
 skills="Java, Spring Boot, Spring MVC, Hibernate, JPA, JSP, Servlets, REST APIs, Microservices, Maven, JUnit, MySQL, Oracle, Tomcat, Git, Jenkins",
 jobs=[("Senior Java Developer", "NetSol Technologies, Lahore", "2021 - Present", ["Designed and developed microservices using Spring Boot and REST APIs for a leasing platform.", "Implemented persistence layer with Hibernate and JPA on Oracle; wrote unit tests with JUnit.", "Set up Maven builds and Jenkins pipelines for continuous integration."]),
       ("Java Developer", "Techlogix, Islamabad", "2019 - 2021", ["Developed JSP and Servlet based web modules and MySQL stored procedures.", "Fixed production defects and improved query performance by 30%."])],
 edu=["BS Computer Science, COMSATS University Islamabad, 2019"],
 projects=["Online banking portal using Spring MVC, Hibernate and MySQL.", "Inventory microservice with Spring Boot, Docker and REST."])
R["Java_Developer_2"] = dict(name="Sara Noman", title="Java Software Engineer", city="Karachi, Pakistan",
 summary="Software engineer who builds back-end systems in Java. Comfortable with object oriented design, SQL databases and agile teams.",
 skills="Core Java, J2EE, Spring, Spring Boot, Hibernate, Struts, JSP, Servlets, JDBC, SQL, PostgreSQL, Maven, Git, Agile, Scrum",
 jobs=[("Java Software Engineer", "10Pearls, Karachi", "2022 - Present", ["Built Spring Boot REST services and JDBC data access code for a healthcare application.", "Wrote JUnit tests and took part in code reviews in an Agile Scrum team."]),
       ("Trainee Engineer", "Netsol, Karachi", "2021 - 2022", ["Learned J2EE, Struts and Hibernate while fixing bugs in a legacy insurance system."])],
 edu=["BS Software Engineering, Karachi University, 2021"],
 projects=["Hospital management system with Java, JSP, Servlets and PostgreSQL.", "Library REST API with Spring Boot and Hibernate."])
R["HR_1"] = dict(name="Mariam Tariq", title="HR Executive", city="Karachi, Pakistan",
 summary="Human resources professional with 4 years of experience in recruitment, onboarding, payroll and employee relations for mid-sized companies.",
 skills="Recruitment, Talent Acquisition, Interviewing, Onboarding, Employee Relations, Payroll, Performance Appraisal, HR Policies, Training and Development, Labour Law, Attendance, HRIS, MS Excel",
 jobs=[("HR Executive", "Engro Foods, Karachi", "2021 - Present", ["Managed full cycle recruitment: job postings, screening resumes, interviewing and offer letters for 60+ hires.", "Ran employee onboarding and induction; maintained employee records in the HRIS.", "Processed monthly payroll and attendance; handled employee grievances and HR policies."]),
       ("HR Assistant", "Dawlance, Karachi", "2019 - 2021", ["Coordinated training and development sessions and performance appraisal cycles.", "Supported labour law compliance and exit interviews."])],
 edu=["MBA Human Resource Management, IBA Karachi, 2019", "BBA, University of Karachi, 2017"],
 projects=["Redesigned the onboarding checklist, cutting new-hire setup time by 25%.", "Introduced an employee engagement survey and action plan."])
R["Web_Designing_1"] = dict(name="Usman Raza", title="Web Designer", city="Lahore, Pakistan",
 summary="Creative web designer who turns ideas into clean, responsive websites. Skilled in HTML, CSS, JavaScript and visual design tools.",
 skills="HTML5, CSS3, JavaScript, jQuery, Bootstrap, Responsive Design, Photoshop, Illustrator, Figma, UI Design, UX, WordPress, SEO, Adobe XD",
 jobs=[("Web Designer", "Creative Hub Agency, Lahore", "2021 - Present", ["Designed and built 25+ responsive websites with HTML, CSS, Bootstrap and JavaScript.", "Created wireframes and mockups in Figma and Photoshop; improved page load time and SEO.", "Customised WordPress themes and landing pages for clients."]),
       ("Junior Designer", "PixelWorks, Lahore", "2019 - 2021", ["Produced banners, logos and UI layouts in Illustrator and Photoshop."])],
 edu=["BS Multimedia and Graphic Design, Beaconhouse National University, 2019"],
 projects=["Portfolio website with animations using CSS3 and jQuery.", "E-commerce landing page redesign that increased conversions."])
R["Web_Designing_2"] = dict(name="Hira Fatima", title="UI/UX and Web Designer", city="Karachi, Pakistan",
 summary="UI designer with an eye for layout and typography, building mobile-first websites and interfaces.",
 skills="HTML, CSS, SASS, JavaScript, Bootstrap, Figma, Adobe XD, Photoshop, UI Design, UX Research, Wireframing, Prototyping, Responsive Design, WordPress, Accessibility",
 jobs=[("UI/UX Designer", "Folio3, Karachi", "2022 - Present", ["Designed wireframes, prototypes and responsive page layouts in Figma and Adobe XD.", "Wrote HTML, CSS and JavaScript for front-end templates; ran usability tests with users."]),
       ("Freelance Web Designer", "Self-employed", "2020 - 2022", ["Delivered 15 WordPress and Bootstrap websites for small businesses."])],
 edu=["BS Computer Science, Iqra University, 2020"],
 projects=["Restaurant ordering website, mobile-first, built with HTML, CSS and JavaScript.", "Design system with reusable UI components in Figma."])
R["Testing_1"] = dict(name="Zainab Khalid", title="Software Test Engineer", city="Islamabad, Pakistan",
 summary="QA engineer with 3 years of experience in manual and automated testing of web applications. Careful, detail oriented and good at writing clear bug reports.",
 skills="Manual Testing, Test Cases, Test Plans, Bug Reporting, Regression Testing, Selenium, Test Automation, JIRA, Postman, API Testing, SQL, SDLC, STLC, Agile, TestNG",
 jobs=[("QA Engineer", "Contour Software, Islamabad", "2022 - Present", ["Wrote test plans and test cases, executed regression testing and logged defects in JIRA.", "Automated login and checkout flows with Selenium and TestNG; tested REST APIs in Postman.", "Verified database results with SQL queries during system and UAT testing."]),
       ("Junior QA Tester", "Cubix, Islamabad", "2021 - 2022", ["Performed functional and smoke testing across the SDLC in an Agile team."])],
 edu=["BS Software Engineering, Air University, 2021"],
 projects=["Selenium test framework for an e-commerce site with reporting.", "API test suite in Postman covering 120 endpoints."])
R["Python_Developer_1"] = dict(name="Ali Hassan", title="Python Developer", city="Lahore, Pakistan",
 summary="Python developer building web back-ends and automation tools. Enjoys clean code, testing and solving practical problems.",
 skills="Python, Django, Flask, FastAPI, REST API, PostgreSQL, SQLAlchemy, Celery, Redis, Docker, Git, Linux, Pytest, HTML, JavaScript",
 jobs=[("Python Developer", "Devsinc, Lahore", "2021 - Present", ["Built Django and FastAPI back-ends with PostgreSQL for a logistics platform.", "Wrote Celery tasks and Redis caching; containerised services with Docker.", "Covered core modules with Pytest and set up Git based workflows."]),
       ("Software Engineer Intern", "Folio3, Lahore", "2020 - 2021", ["Automated reports with Python scripts and Flask tools."])],
 edu=["BS Computer Science, LUMS, 2020"],
 projects=["Expense tracker REST API with Flask and SQLAlchemy.", "Web scraper and dashboard built with Django."])
R["DevOps_Engineer_1"] = dict(name="Omar Farooq", title="DevOps Engineer", city="Karachi, Pakistan",
 summary="DevOps engineer who automates builds, deployments and infrastructure on AWS. Focus on reliability and fast releases.",
 skills="AWS, Docker, Kubernetes, Jenkins, CI/CD, Terraform, Ansible, Linux, Bash, Python, Git, Prometheus, Grafana, Nginx, Monitoring, Infrastructure as Code",
 jobs=[("DevOps Engineer", "Careem, Karachi", "2021 - Present", ["Built CI/CD pipelines with Jenkins and Git; cut release time from 2 hours to 15 minutes.", "Managed Kubernetes clusters and Docker images on AWS; wrote Terraform and Ansible scripts.", "Set up Prometheus and Grafana monitoring and on-call alerts."]),
       ("System Administrator", "Jazz, Karachi", "2019 - 2021", ["Administered Linux servers, Nginx and Bash automation."])],
 edu=["BS Electrical Engineering, NED University, 2019"],
 projects=["Terraform modules for a three-tier AWS environment.", "Zero-downtime deployments with Kubernetes rolling updates."])
R["Database_1"] = dict(name="Nida Shahid", title="Database Administrator", city="Islamabad, Pakistan",
 summary="Database administrator with 5 years of experience tuning and securing SQL databases.",
 skills="SQL, MySQL, Oracle, PostgreSQL, SQL Server, PL/SQL, T-SQL, Database Design, Backup and Recovery, Performance Tuning, Indexing, Stored Procedures, Replication, Data Modelling",
 jobs=[("Database Administrator", "Habib Bank, Islamabad", "2020 - Present", ["Administered Oracle and SQL Server databases; scheduled backup and recovery and replication.", "Tuned slow queries with indexing and execution plans, improving report speed by 40%.", "Wrote PL/SQL stored procedures and data models."]),
       ("SQL Developer", "Systems Limited, Lahore", "2018 - 2020", ["Designed MySQL schemas and T-SQL procedures for finance applications."])],
 edu=["BS Information Technology, Quaid-i-Azam University, 2018"],
 projects=["Migrated a MySQL system to PostgreSQL with zero data loss.", "Built a data warehouse schema for sales reporting."])
R["Business_Analyst_1"] = dict(name="Fahad Mehmood", title="Business Analyst", city="Karachi, Pakistan",
 summary="Business analyst who gathers requirements, models processes and works with developers and stakeholders to deliver useful software.",
 skills="Requirements Gathering, Stakeholder Management, BRD, FRD, User Stories, UML, Process Modelling, Use Cases, SQL, JIRA, Agile, Scrum, MS Visio, Gap Analysis, UAT",
 jobs=[("Business Analyst", "Allied Bank, Karachi", "2021 - Present", ["Gathered requirements from stakeholders and wrote BRD, FRD and user stories for a mobile banking app.", "Modelled processes in UML and Visio; ran gap analysis and supported UAT.", "Managed the backlog in JIRA in an Agile Scrum team; used SQL for data checks."]),
       ("Junior Business Analyst", "Askari Bank, Karachi", "2019 - 2021", ["Documented use cases and process flows for loan systems."])],
 edu=["MBA, IBA Karachi, 2019", "BBA, Institute of Business Management, 2017"],
 projects=["Redesigned the account opening process, reducing steps by 30%.", "Requirements package for a customer complaints portal."])

DARK, GREY = colors.HexColor("#1f3a5f"), colors.HexColor("#555555")
ss = getSampleStyleSheet()
NAME = ParagraphStyle("n", parent=ss["Title"], fontSize=22, textColor=DARK, alignment=0, spaceAfter=0)
ROLE = ParagraphStyle("r", parent=ss["Normal"], fontSize=12, textColor=GREY, spaceAfter=2)
SMALL = ParagraphStyle("s", parent=ss["Normal"], fontSize=9, textColor=GREY)
HEAD = ParagraphStyle("h", parent=ss["Heading2"], fontSize=11, textColor=DARK, spaceBefore=10, spaceAfter=2)
BODY = ParagraphStyle("b", parent=ss["Normal"], fontSize=10, leading=13)
BOLD = ParagraphStyle("bb", parent=BODY, fontName="Helvetica-Bold")


def build(key, d):
    first = d["name"].split()[0].lower()
    last = d["name"].split()[-1].lower()
    phone = "+92 3" + str(abs(hash(key)) % 90 + 10) + " " + str(1000000 + abs(hash(key[::-1])) % 8999999)
    contact = f"{d['city']}  |  {first}.{last}@example.com  |  {phone}"
    out = [Paragraph(d["name"], NAME), Paragraph(d["title"], ROLE), Paragraph(contact, SMALL),
           HRFlowable(width="100%", thickness=1.2, color=DARK, spaceBefore=6)]
    out += [Paragraph("PROFESSIONAL SUMMARY", HEAD), Paragraph(d["summary"], BODY)]
    out += [Paragraph("SKILLS", HEAD), Paragraph(d["skills"], BODY)]
    out += [Paragraph("EXPERIENCE", HEAD)]
    for role, company, dates, bullets in d["jobs"]:
        out += [Paragraph(f"{role} - {company}", BOLD), Paragraph(dates, SMALL),
                ListFlowable([ListItem(Paragraph(b, BODY), leftIndent=12) for b in bullets], bulletType="bullet", start="•", leftIndent=12),
                Spacer(1, 4)]
    out += [Paragraph("PROJECTS", HEAD),
            ListFlowable([ListItem(Paragraph(b, BODY), leftIndent=12) for b in d["projects"]], bulletType="bullet", start="•", leftIndent=12)]
    out += [Paragraph("EDUCATION", HEAD)] + [Paragraph(e, BODY) for e in d["edu"]]
    os.makedirs("sample_resumes", exist_ok=True)
    SimpleDocTemplate(f"sample_resumes/{key}.pdf", pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=15 * mm, bottomMargin=15 * mm, title=f"{d['name']} - Resume", author=d["name"]).build(out)


for k, v in R.items():
    build(k, v)
print(f"Created {len(R)} sample resumes in sample_resumes/ (all people are fictional).")
