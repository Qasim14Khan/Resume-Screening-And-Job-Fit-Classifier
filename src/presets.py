"""Job descriptions for the dashboard's drop-down list. Users pick a title and can edit the description."""

JOB_PRESETS = {
    "Backend Developer": ("We are hiring a Backend Developer. Required: python, java, node, rest api, sql, postgresql, "
                          "mysql, microservices, docker, authentication, git and unit testing."),
    "Business Analyst": ("We are hiring a Business Analyst. Required: requirements gathering, stakeholder management, "
                         "user stories, process modelling, uml, use cases, sql, jira, agile and uat."),
    "Data Analyst": ("We are hiring a Data Analyst. Required: sql, excel, power bi, tableau, python, pandas, "
                     "statistics, data visualization, reporting and data cleaning."),
    "Data Scientist": ("We are hiring a Data Scientist. Required: python, pandas, numpy, machine learning, "
                       "statistics, scikit-learn, sql, data visualization and tensorflow."),
    "Database Administrator": ("We are hiring a Database Administrator. Required: sql, oracle, mysql, postgresql, "
                               "backup and recovery, performance tuning, indexing, stored procedures and replication."),
    "DevOps Engineer": ("We are hiring a DevOps Engineer. Required: aws, docker, kubernetes, jenkins, ci/cd, "
                        "terraform, ansible, linux, git, monitoring and bash scripting."),
    "Frontend Developer": ("We are hiring a Frontend Developer. Required: html, css, javascript, typescript, react, "
                           "responsive design, bootstrap, rest api, git and ui design."),
    "Full Stack Developer": ("We are hiring a Full Stack Developer. Required: html, css, javascript, react, node, "
                             "python, rest api, sql, mongodb, git and docker."),
    "HR Executive": ("We are hiring an HR Executive. Required: recruitment, onboarding, payroll, employee "
                     "relations, training and talent management."),
    "Java Developer": ("We are hiring a Java Developer. Required: java, spring, hibernate, sql, jsp, servlets, "
                       "maven, rest api and microservices."),
    "Machine Learning Engineer": ("We are hiring a Machine Learning Engineer. Required: python, machine learning, "
                                  "deep learning, tensorflow, pytorch, scikit-learn, nlp, docker and model deployment."),
    "Network Security Engineer": ("We are hiring a Network Security Engineer. Required: cisco, firewall, network "
                                  "security, vpn, switches, routing, troubleshooting, siem and incident response."),
    "Operations Manager": ("We are hiring an Operations Manager. Required: operations management, process "
                           "improvement, team leadership, budgeting, reporting, vendor management and quality control."),
    "Project Manager": ("We are hiring a Project Manager. Required: project management, agile, scrum, risk management, "
                        "stakeholder management, project planning, budgeting, jira and reporting."),
    "Python Developer": ("We are hiring a Python Developer. Required: python, django, flask, fastapi, rest api, "
                         "sql, postgresql, docker, git and pytest."),
    "Sales Manager": ("We are hiring a Sales Manager. Required: sales, lead generation, business development, "
                      "client relationships, negotiation, crm, target achievement and team leadership."),
    "Software Tester": ("We are hiring a Software Tester. Required: manual testing, test cases, selenium, "
                        "automation testing, bug tracking, jira and sql."),
    "Web Designer": ("We are hiring a Web Designer. Required: html, css, javascript, jquery, bootstrap, "
                     "photoshop and responsive design."),
}

JOB_PRESETS.update({
    "Android Developer": ("We are hiring an Android Developer. Required: android, kotlin, java, android studio, "
                          "rest api, jetpack, firebase, sqlite, git and ui design."),
    "iOS Developer": ("We are hiring an iOS Developer. Required: ios, swift, objective-c, xcode, swiftui, "
                      "rest api, core data, git and app store."),
    "DotNet Developer": ("We are hiring a DotNet Developer. Required: c#, asp.net, mvc, .net core, entity framework, "
                         "sql server, rest api, git and azure."),
    "SAP Developer": ("We are hiring a SAP Developer. Required: sap, abap, hana, sap bo, sap fiori, "
                      "sql, reporting, integration and support."),
    "ETL Developer": ("We are hiring an ETL Developer. Required: etl, informatica, sql, data warehouse, "
                      "data modelling, unix, mappings, scheduling and data quality."),
    "Big Data Engineer": ("We are hiring a Big Data Engineer. Required: hadoop, spark, hive, hdfs, sqoop, "
                          "mapreduce, kafka, python, sql and data pipelines."),
    "Blockchain Developer": ("We are hiring a Blockchain Developer. Required: blockchain, ethereum, solidity, "
                             "smart contracts, web3, cryptography, javascript and decentralized applications."),
    "Cloud Engineer": ("We are hiring a Cloud Engineer. Required: aws, azure, cloud computing, networking, "
                       "linux, terraform, docker, security and monitoring."),
    "Cybersecurity Analyst": ("We are hiring a Cybersecurity Analyst. Required: cybersecurity, siem, incident "
                              "response, vulnerability assessment, penetration testing, firewall and risk assessment."),
    "QA Automation Engineer": ("We are hiring a QA Automation Engineer. Required: automation testing, selenium, "
                               "testng, api testing, postman, ci/cd, jira, java or python and test frameworks."),
    "UI/UX Designer": ("We are hiring a UI/UX Designer. Required: figma, adobe xd, wireframing, prototyping, "
                       "user research, usability testing, design systems and responsive design."),
    "Graphic Designer": ("We are hiring a Graphic Designer. Required: photoshop, illustrator, indesign, branding, "
                         "logo design, typography, layout and social media design."),
    "Digital Marketing Executive": ("We are hiring a Digital Marketing Executive. Required: seo, social media, "
                                    "google ads, content marketing, email marketing, analytics and campaign management."),
    "Marketing Manager": ("We are hiring a Marketing Manager. Required: marketing strategy, brand management, "
                          "campaign management, market research, budgeting, analytics and team leadership."),
    "Product Manager": ("We are hiring a Product Manager. Required: product management, roadmap, user stories, "
                        "stakeholder management, agile, market research, analytics and prioritization."),
    "Accountant": ("We are hiring an Accountant. Required: accounting, bookkeeping, financial reporting, "
                   "taxation, accounts payable, accounts receivable, reconciliation, excel and audit."),
    "Customer Support Executive": ("We are hiring a Customer Support Executive. Required: customer service, "
                                   "communication, complaint handling, crm, ticketing, problem solving and email support."),
    "Content Writer": ("We are hiring a Content Writer. Required: content writing, copywriting, seo, editing, "
                       "proofreading, research, blogging and social media content."),
    "Civil Engineer": ("We are hiring a Civil Engineer. Required: civil engineering, site supervision, autocad, "
                       "construction, estimation, structural design, quantity surveying and project planning."),
    "Mechanical Engineer": ("We are hiring a Mechanical Engineer. Required: mechanical engineering, autocad, "
                            "solidworks, design, manufacturing, maintenance, thermodynamics and quality control."),
    "Electrical Engineer": ("We are hiring an Electrical Engineer. Required: electrical engineering, power systems, "
                            "circuit design, plc, maintenance, safety, autocad and testing."),
    "Advocate": ("We are hiring an Advocate. Required: legal research, litigation, court, drafting, contracts, "
                 "legal advice, case management and client representation."),
})
JOB_PRESETS = dict(sorted(JOB_PRESETS.items(), key=lambda kv: kv[0].lower()))
