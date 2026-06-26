import json
import random
import google.generativeai as genai

from app.core.config import settings

genai.configure(api_key=settings.gemini_api_key)

PREDEFINED_QUESTIONS = {
    "SQL": [
        {
            "question_text": "What is the difference between WHERE and HAVING clauses in SQL?",
            "ideal_answer": "WHERE is used to filter rows before any groupings are made, whereas HAVING is used to filter groups after the GROUP BY clause has been applied. WHERE cannot contain aggregate functions, while HAVING is designed to filter based on aggregate results.",
            "keywords": ["group", "aggregate", "row"],
            "topic": "WHERE vs HAVING clauses"
        },
        {
            "question_text": "Explain the difference between primary keys, foreign keys, and unique keys.",
            "ideal_answer": "A Primary Key uniquely identifies each row in a table and cannot contain NULL values. A Foreign Key is a field in one table that refers to the Primary Key in another table, creating a relationship. A Unique Key ensures all values in a column are distinct, but unlike a Primary Key, it can allow a NULL value.",
            "keywords": ["identify", "null", "refer"],
            "topic": "Database Keys (Primary, Foreign, Unique)"
        },
        {
            "question_text": "What are indexes, and how do they improve database query performance?",
            "ideal_answer": "An index is a database structure (typically a B-Tree) that improves data retrieval speed by providing a fast lookup path instead of performing full table scans. However, indexes slow down write operations (INSERT, UPDATE, DELETE) because the index must be updated.",
            "keywords": ["speed", "write", "scan"],
            "topic": "Database Indexes and Performance"
        },
        {
            "question_text": "Describe the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN.",
            "ideal_answer": "INNER JOIN returns only rows that have matching values in both tables. LEFT JOIN returns all rows from the left table, and matching rows from the right table (with NULLs for non-matching right rows). RIGHT JOIN returns all rows from the right table, and matching rows from the left table (with NULLs for non-matching left rows).",
            "keywords": ["match", "null", "all"],
            "topic": "SQL Joins (INNER, LEFT, RIGHT)"
        },
        {
            "question_text": "What is database normalization, and what are the first three normal forms?",
            "ideal_answer": "Database normalization is the process of structuring a database to reduce data redundancy and improve data integrity. 1NF requires atomic values and no repeating groups. 2NF requires being in 1NF and all non-key columns being fully dependent on the primary key. 3NF requires being in 2NF and having no transitive dependencies.",
            "keywords": ["redundancy", "atomic", "transitive"],
            "topic": "Database Normalization"
        },
        {
            "question_text": "How do you find duplicate records in a SQL table?",
            "ideal_answer": "You can find duplicates by using GROUP BY on the columns you want to check for duplicates, and using HAVING COUNT(*) > 1 to filter out unique records. For example: SELECT col, COUNT(*) FROM table GROUP BY col HAVING COUNT(*) > 1.",
            "keywords": ["group", "having", "count"],
            "topic": "Finding Duplicate Records"
        },
        {
            "question_text": "What is the difference between UNION and UNION ALL?",
            "ideal_answer": "UNION combines the result sets of two or more SELECT queries and removes duplicate rows from the final result. UNION ALL combines the result sets and retains all duplicate rows, making it faster since it does not perform a sorting/deduplication step.",
            "keywords": ["remove", "retain", "speed"],
            "topic": "UNION vs UNION ALL"
        },
        {
            "question_text": "Explain ACID properties in database management systems.",
            "ideal_answer": "ACID stands for Atomicity (all operations in a transaction succeed or all fail), Consistency (transaction leaves database in a valid state), Isolation (transactions execute independently without interference), and Durability (once committed, changes are permanent even during power loss).",
            "keywords": ["atomicity", "isolation", "durability"],
            "topic": "ACID properties"
        }
    ],
    "Java": [
        {
            "question_text": "Explain the difference between JDK, JRE, and JVM.",
            "ideal_answer": "JVM (Java Virtual Machine) executes bytecode. JRE (Java Runtime Environment) contains the JVM plus libraries to run Java apps. JDK (Java Development Kit) is a full SDK including the JRE and development tools like compilers (javac) and debuggers.",
            "keywords": ["execute", "compiler", "libraries"],
            "topic": "JDK, JRE, and JVM relationships"
        },
        {
            "question_text": "What are the OOP principles, and how are they implemented in Java?",
            "ideal_answer": "The four principles are: Encapsulation (using private variables and public getters/setters), Inheritance (using the 'extends' keyword), Polymorphism (method overloading and overriding), and Abstraction (using abstract classes and interfaces).",
            "keywords": ["encapsulation", "inheritance", "polymorphism", "abstraction"],
            "topic": "Object-Oriented Programming (OOP)"
        },
        {
            "question_text": "What is the difference between an abstract class and an interface in Java?",
            "ideal_answer": "An abstract class can have instance variables, constructors, and both abstract and concrete methods. An interface (prior to Java 8) could only have abstract methods and public static final constants. A class can implement multiple interfaces, but extend only one class.",
            "keywords": ["multiple", "variables", "concrete"],
            "topic": "Abstract Classes vs Interfaces"
        },
        {
            "question_text": "How does the Java Garbage Collector work?",
            "ideal_answer": "Java Garbage Collection is an automatic process that reclaims heap memory by destroying unreachable objects. It uses a generational hypothesis, dividing the heap into Young Generation (Eden, survivor spaces) and Old Generation, performing minor and major collections.",
            "keywords": ["heap", "automatic", "generation"],
            "topic": "Garbage Collection mechanics"
        },
        {
            "question_text": "Explain the difference between ArrayList and LinkedList.",
            "ideal_answer": "ArrayList is backed by a dynamic array, providing O(1) random access but O(n) insertion/deletion in the middle. LinkedList is backed by a doubly-linked list, providing O(1) insertion/deletion once the node is located but O(n) search time.",
            "keywords": ["array", "list", "access"],
            "topic": "ArrayList vs LinkedList"
        },
        {
            "question_text": "What is the difference between == and equals() method in Java?",
            "ideal_answer": "== compares reference equality (whether two variables point to the same memory location). The equals() method compares content equality (whether the values inside the objects are equivalent), and should be overridden for custom classes.",
            "keywords": ["reference", "content", "override"],
            "topic": "Comparison using == vs equals()"
        },
        {
            "question_text": "Explain exception handling in Java. What is the difference between checked and unchecked exceptions?",
            "ideal_answer": "Checked exceptions are checked at compile-time and must be handled using try-catch or declared in the throws clause (e.g., IOException). Unchecked exceptions extend RuntimeException and are checked at runtime, representing bugs (e.g., NullPointerException).",
            "keywords": ["compile", "runtime", "runtimeexception"],
            "topic": "Checked vs Unchecked Exceptions"
        },
        {
            "question_text": "What is the purpose of the volatile keyword in Java?",
            "ideal_answer": "The volatile keyword is used in multithreading to mark a Java variable as stored in main memory, meaning that every read will be from main memory and every write will write back to main memory, ensuring visibility across threads.",
            "keywords": ["thread", "memory", "visibility"],
            "topic": "The volatile keyword"
        }
    ],
    "Spring Boot": [
        {
            "question_text": "What is Dependency Injection, and how does Spring Boot implement it?",
            "ideal_answer": "Dependency Injection (DI) is a pattern where object dependencies are provided by the container rather than created by the object itself. Spring Boot implements DI using its Inversion of Control (IoC) container via constructor, setter, or field injection.",
            "keywords": ["container", "constructor", "control"],
            "topic": "Dependency Injection in Spring"
        },
        {
            "question_text": "Explain the Spring Boot application lifecycle.",
            "ideal_answer": "The lifecycle starts with running SpringApplication.run(), which initializes the ApplicationContext, runs context initializers, starts the embedded web container (e.g., Tomcat), and fires application events like ApplicationReadyEvent before starting.",
            "keywords": ["context", "run", "tomcat"],
            "topic": "Spring Boot App Lifecycle"
        },
        {
            "question_text": "What is the difference between @Component, @Service, and @Repository annotations?",
            "ideal_answer": "@Component is the generic stereotype annotation for any Spring-managed bean. @Service specializes it for service/business logic. @Repository specializes it for database access layer, automatically translating database exceptions into Spring's DataAccessException.",
            "keywords": ["stereotype", "exception", "business"],
            "topic": "Spring Stereotype Annotations"
        },
        {
            "question_text": "How does Spring Boot Autoconfiguration work?",
            "ideal_answer": "Spring Boot looks at the classpath dependencies (e.g., spring-boot-starter-web) and automatically configures beans based on annotations like @ConditionalOnClass and @ConditionalOnMissingBean. This is enabled by @EnableAutoConfiguration.",
            "keywords": ["classpath", "conditional", "enable"],
            "topic": "Spring Boot Autoconfiguration"
        },
        {
            "question_text": "Explain the difference between @Controller and @RestController.",
            "ideal_answer": "@Controller is used for traditional MVC controllers that return view names (like HTML pages). @RestController is a convenience annotation that combines @Controller and @ResponseBody, meaning it serializes response objects directly into JSON/XML.",
            "keywords": ["responsebody", "view", "json"],
            "topic": "@Controller vs @RestController"
        },
        {
            "question_text": "How do you handle exceptions globally in a Spring Boot application?",
            "ideal_answer": "You use a class annotated with @ControllerAdvice or @RestControllerAdvice, containing methods annotated with @ExceptionHandler specifying the target exception types. These methods format and return error payloads.",
            "keywords": ["advice", "handler", "global"],
            "topic": "Global Exception Handling in Spring Boot"
        },
        {
            "question_text": "What is Spring Data JPA, and how does it simplify database operations?",
            "ideal_answer": "Spring Data JPA reduces boilerplate code by generating repository implementations at runtime from interface declarations. It provides standard CRUD methods and allows creating custom queries by using method naming conventions.",
            "keywords": ["boilerplate", "interface", "naming"],
            "topic": "Spring Data JPA"
        },
        {
            "question_text": "How do you secure a Spring Boot application using Spring Security?",
            "ideal_answer": "Spring Security uses a chain of Servlet Filters to intercept requests. You configure authentication (e.g., JDBC, LDAP, JWT) and authorization rules by defining a SecurityFilterChain bean and using method annotations like @PreAuthorize.",
            "keywords": ["filter", "chain", "authorization"],
            "topic": "Spring Security mechanics"
        }
    ],
    "React": [
        {
            "question_text": "What is the Virtual DOM, and how does React use it to render pages?",
            "ideal_answer": "The Virtual DOM is a lightweight, in-memory representation of the real DOM. When state changes, React creates a new virtual DOM tree, compares it with the previous one (diffing), and batch updates only the changed parts of the real DOM (reconciliation).",
            "keywords": ["diff", "reconciliation", "memory"],
            "topic": "React's Virtual DOM"
        },
        {
            "question_text": "Explain the React component lifecycle or equivalent hooks functional approach.",
            "ideal_answer": "In functional components, hooks replace lifecycle methods. Mounting is handled by useEffect with an empty dependency array []. Updating is handled by useEffect when variables in the dependency array change. Unmounting is handled by the cleanup function returned by useEffect.",
            "keywords": ["mounting", "cleanup", "updating"],
            "topic": "React Component Lifecycle with Hooks"
        },
        {
            "question_text": "What is the difference between state and props in React?",
            "ideal_answer": "Props (properties) are read-only inputs passed from a parent component down to a child, and are immutable within that child. State is local, mutable data managed internally by the component itself, and changes trigger re-rendering.",
            "keywords": ["immutable", "mutable", "render"],
            "topic": "State vs Props in React"
        },
        {
            "question_text": "Explain the purpose and usage of the useEffect hook.",
            "ideal_answer": "The useEffect hook lets you perform side effects (data fetching, subscriptions, manual DOM updates) in functional components. It runs after render, and its execution can be optimized using a dependency array.",
            "keywords": ["side effect", "render", "dependency"],
            "topic": "React's useEffect Hook"
        },
        {
            "question_text": "How does React's Context API work, and when should you use it?",
            "ideal_answer": "Context API provides a way to pass data through the component tree without prop-drilling manually at every level. You should use it for global data that is shared by many components, such as themes, user authentication, or locale settings.",
            "keywords": ["prop-drilling", "provider", "global"],
            "topic": "React's Context API"
        },
        {
            "question_text": "What are React Server Components (RSC) and how do they differ from client components?",
            "ideal_answer": "React Server Components render entirely on the server, sending zero client-side JavaScript for the component logic, improving load times. Client components are the traditional components that run and re-render in the browser.",
            "keywords": ["server", "javascript", "client"],
            "topic": "React Server Components (RSC)"
        },
        {
            "question_text": "Explain the difference between useMemo and useCallback hooks.",
            "ideal_answer": "useMemo memoizes the computed value of a function, re-evaluating it only when dependencies change. useCallback memoizes the function definition itself, preventing unnecessary recreations on every render.",
            "keywords": ["value", "definition", "render"],
            "topic": "useMemo vs useCallback Hooks"
        },
        {
            "question_text": "How do you handle global state management in React applications?",
            "ideal_answer": "Global state can be managed using React Context for simple states, or external libraries like Redux Toolkit, Zustand, Recoil, or MobX for more complex, high-performance global state requirements.",
            "keywords": ["context", "redux", "zustand"],
            "topic": "Global State Management in React"
        }
    ],
    "DSA": [
        {
            "question_text": "What is Big O notation, and how do you analyze time complexity?",
            "ideal_answer": "Big O notation describes the upper bound of an algorithm's running time or space requirements as a function of the input size (n). It focuses on the worst-case scenario and ignores constant factors and lower-order terms.",
            "keywords": ["upper", "worst", "factors"],
            "topic": "Big O notation"
        },
        {
            "question_text": "Explain the difference between a stack and a queue data structure.",
            "ideal_answer": "A stack is a Last-In-First-Out (LIFO) data structure where elements are pushed and popped from the same end. A queue is a First-In-First-Out (FIFO) data structure where elements are inserted at the rear (enqueue) and removed from the front (dequeue).",
            "keywords": ["lifo", "fifo", "end"],
            "topic": "Stacks vs Queues"
        },
        {
            "question_text": "How does the binary search algorithm work, and what is its time complexity?",
            "ideal_answer": "Binary search works on a sorted array by repeatedly dividing the search interval in half. If the target is less than the middle element, it searches the lower half; otherwise, the upper half. Its time complexity is O(log n).",
            "keywords": ["sorted", "half", "log"],
            "topic": "Binary Search Algorithm"
        },
        {
            "question_text": "Explain the difference between BFS (Breadth-First Search) and DFS (Depth-First Search).",
            "ideal_answer": "BFS explores a graph level-by-level using a queue, finding the shortest path in unweighted graphs. DFS explores deep along each branch before backtracking, utilizing a stack or recursion.",
            "keywords": ["queue", "stack", "shortest"],
            "topic": "BFS vs DFS Graph Searches"
        },
        {
            "question_text": "What is a hash table, and how are collisions resolved?",
            "ideal_answer": "A hash table maps keys to array indices using a hash function. Collisions (different keys hashing to the same index) are resolved using Chaining (linked lists at each index) or Open Addressing (finding another free slot via linear/quadratic probing).",
            "keywords": ["hash", "chaining", "addressing"],
            "topic": "Hash Tables and Collision Resolution"
        },
        {
            "question_text": "Describe how the QuickSort sorting algorithm works.",
            "ideal_answer": "QuickSort is a divide-and-conquer algorithm. It selects a pivot, partitions the array such that elements smaller than the pivot go to the left and larger elements go to the right, and then recursively sorts the sub-arrays. Average time complexity is O(n log n).",
            "keywords": ["pivot", "partition", "log"],
            "topic": "QuickSort Sorting Algorithm"
        },
        {
            "question_text": "What is dynamic programming, and how does it differ from recursion?",
            "ideal_answer": "Dynamic programming solves optimization problems by breaking them into overlapping subproblems, solving each subproblem once, and storing their solutions (memoization/tabulation) to avoid redundant computations, unlike simple recursion.",
            "keywords": ["overlapping", "memoization", "recursion"],
            "topic": "Dynamic Programming principles"
        },
        {
            "question_text": "Explain the concept of a binary search tree (BST) and its operations.",
            "ideal_answer": "A BST is a binary tree where each node's left child has a value less than the node, and the right child has a value greater. Search, insert, and delete operations take O(log n) time on average, but can degrade to O(n) if the tree is unbalanced.",
            "keywords": ["less", "greater", "unbalanced"],
            "topic": "Binary Search Trees (BST)"
        }
    ],
    "HR": [
        {
            "question_text": "Tell me about yourself and your background.",
            "ideal_answer": "A strong response follows the Present-Past-Future formula: start with your current role and recent achievements, talk about key past experiences that led you here, and end with why you are excited about this specific opportunity.",
            "keywords": ["present", "past", "future"],
            "topic": "Self-introduction pitch"
        },
        {
            "question_text": "Why do you want to join our company?",
            "ideal_answer": "Demonstrate research by citing the company's culture, mission, technical stack, or recent news. Align these with your own career goals, showing how you can add value to their team and grow alongside them.",
            "keywords": ["research", "value", "grow"],
            "topic": "Alignment with company goals"
        },
        {
            "question_text": "Describe a time you faced a difficult technical challenge and how you overcame it.",
            "ideal_answer": "Use the STAR method. Describe the task/challenge, the options you considered, the specific action you took (collaborating, researching documentation, testing), and the positive quantifiable outcome.",
            "keywords": ["star", "action", "outcome"],
            "topic": "Technical challenge resolution"
        },
        {
            "question_text": "How do you handle conflict or disagreement with a team member?",
            "ideal_answer": "Explain that you handle conflict professionally by listening actively to their perspective, focusing on data and facts rather than emotions, discussing alternatives, and aligning on what is best for the project/team.",
            "keywords": ["listen", "professional", "align"],
            "topic": "Conflict management"
        },
        {
            "question_text": "Where do you see yourself in five years?",
            "ideal_answer": "Express a desire to grow technically and professionally, take on more ownership or leadership responsibilities, and become a key contributor within the company, showing commitment to long-term growth.",
            "keywords": ["leadership", "growth", "commit"],
            "topic": "Five-year career vision"
        },
        {
            "question_text": "What are your greatest strengths and weaknesses?",
            "ideal_answer": "For strengths, name a relevant skill (e.g., problem-solving, collaboration) and give an example. For weaknesses, state a genuine area of improvement (e.g., public speaking) and describe the proactive steps you are taking to address it.",
            "keywords": ["strength", "weakness", "improvement"],
            "topic": "Self-assessment (Strengths & Weaknesses)"
        },
        {
            "question_text": "Describe a situation where you had to work under a tight deadline.",
            "ideal_answer": "Describe a situation where a tight deadline was set. Explain how you prioritized tasks, managed expectations, communicated clearly with stakeholders, worked efficiently, and delivered the project on time.",
            "keywords": ["prioritize", "communicate", "expectations"],
            "topic": "Working under tight deadlines"
        },
        {
            "question_text": "Why should we hire you over other candidates?",
            "ideal_answer": "Connect your unique blend of technical skills, enthusiasm, problem-solving mindset, and alignment with the company's culture. Emphasize that you are ready to hit the ground running and make an immediate impact.",
            "keywords": ["unique", "impact", "culture"],
            "topic": "Candidate value proposition"
        }
    ]
}


class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.gemini_model)

    def generate_questions(
        self, domain: str, difficulty: str, total_questions: int
    ) -> list[dict]:
        prompt = (
            f"Generate a JSON object with a 'questions' array. Each item in the array must be a JSON object with the following fields:\n"
            f"1. 'question_text': A practical, concise, and professional {difficulty} interview question for the {domain} domain.\n"
            f"2. 'ideal_answer': A detailed, accurate ideal answer that explains how a candidate should answer this question to score 100%.\n"
            f"3. 'keywords': A JSON list of 3-5 core technical terms, APIs, or key concepts that are essential to be mentioned in a correct answer (use single words or very short phrases in lowercase, e.g. ['where', 'having'] or ['virtual dom', 'diffing']).\n\n"
            f"Generate exactly {total_questions} questions.\n"
            "CRITICAL: Every question generated must be completely unique and cover a different topic or concept within the domain. Do NOT repeat questions or ask about the same concept twice.\n"
            "Return ONLY the raw JSON object, without any explanation or markdown formatting."
        )
        data = self._json_response(prompt)
        questions = data.get("questions", [])
        if not isinstance(questions, list) or not questions:
            return self._fallback_questions(domain, total_questions)

        valid_qs = []
        seen_questions = set()
        for q in questions:
            if isinstance(q, dict) and "question_text" in q:
                q_text = str(q["question_text"]).strip()
                if q_text.lower() not in seen_questions:
                    seen_questions.add(q_text.lower())
                    valid_qs.append({
                        "question_text": q_text,
                        "ideal_answer": str(q.get("ideal_answer", "No ideal answer available.")),
                        "keywords": q.get("keywords", [])
                    })
        if len(valid_qs) < total_questions:
            # fill with fallback if we didn't get enough
            fb = self._fallback_questions(domain, total_questions - len(valid_qs))
            valid_qs.extend(fb)
        return valid_qs[:total_questions]

    def evaluate_interview(
        self, domain: str, difficulty: str, questions: list
    ) -> dict:
        interview_data = []
        for q in questions:
            # Parse keywords if stored as string JSON
            kws = []
            if q.keywords:
                try:
                    kws = json.loads(q.keywords)
                except Exception:
                    kws = [k.strip() for k in q.keywords.split(",") if k.strip()]
            
            interview_data.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "user_answer": q.user_answer or "Not answered",
                "ideal_answer": q.ideal_answer or "No ideal answer available.",
                "keywords": kws
            })
            
        prompt = (
            "You are an expert technical interviewer. Evaluate the candidate's answers for a mock interview.\n"
            f"Domain: {domain}\n"
            f"Difficulty: {difficulty}\n\n"
            "Evaluate each question individually based on the candidate's answer vs the ideal answer and keywords. "
            "Write a proper dedicated feedback for each question. The feedback must contain two distinct items:\n"
            "1. feedback_critique: A detailed critique pointing out what they did well, and what key concepts/points they missed or got wrong compared to the ideal answer.\n"
            "2. feedback_improvement: Actionable, specific suggestions on how the candidate could have answered the question better, including technical details they should have included.\n\n"
            "Here is the interview data:\n"
            f"{json.dumps(interview_data, indent=2)}\n\n"
            "Return ONLY a JSON object with this exact structure:\n"
            "{\n"
            "  \"overall_score\": <number from 0 to 100 representing overall performance across all questions>,\n"
            "  \"strengths\": [\n"
            "    \"strength point 1 (be specific to this interview context)\",\n"
            "    \"strength point 2\"\n"
            "  ],\n"
            "  \"weaknesses\": [\n"
            "    \"weakness point 1 (be specific to this interview context)\",\n"
            "    \"weakness point 2\"\n"
            "  ],\n"
            "  \"recommendations\": [\n"
            "    \"recommendation point 1 (actionable study steps)\",\n"
            "    \"recommendation point 2\"\n"
            "  ],\n"
            "  \"question_scores\": [\n"
            "    {\n"
            "      \"question_id\": <matching question_id integer>,\n"
            "      \"score\": <number from 0 to 100 based on answer completeness and correctness compared to ideal answer>,\n"
            "      \"feedback_critique\": \"[Detailed critique comparing user answer to ideal answer, pointing out what was correct and what was missed]\",\n"
            "      \"feedback_improvement\": \"[Actionable advice on how the candidate could have answered the question better]\"\n"
            "    }\n"
            "  ]\n"
            "}\n"
        )
        
        data = self._json_response(prompt)
        
        # Check if the API call failed (empty dict returned due to rate limiting/error)
        if not data:
            question_scores = []
            total_score = 0.0
            
            strengths_list = []
            weaknesses_list = []
            recommendations_list = []
            
            for q in questions:
                user_ans = (q.user_answer or "").strip()
                ideal_ans = q.ideal_answer or "No ideal answer available."
                
                # Load keywords
                kws = []
                if q.keywords:
                    try:
                        kws = json.loads(q.keywords)
                        if not isinstance(kws, list):
                            kws = [kws]
                    except Exception:
                        kws = [k.strip() for k in q.keywords.split(",") if k.strip()]
                
                # Look up topic/details if fallback matching matches
                topic_name = "Core Technical Concept"
                matched_q = None
                for domain_list in PREDEFINED_QUESTIONS.values():
                    for pq in domain_list:
                        if pq["question_text"].lower() == q.question_text.lower():
                            matched_q = pq
                            break
                    if matched_q:
                        break
                
                if matched_q:
                    topic_name = matched_q.get("topic", topic_name)
                    if not kws:
                        kws = matched_q["keywords"]
                    if ideal_ans == "No ideal answer available.":
                        ideal_ans = matched_q["ideal_answer"]
                
                if not kws:
                    kws = ["concept", "detail", "explanation"]
                
                if not user_ans or len(user_ans) < 5:
                    score = 0.0
                    feedback_critique = "No answer was provided. To evaluate this question, you need to attempt to write a response."
                    feedback_improvement = f"To answer this question, you should describe the core principles. Here is the ideal answer structure: {ideal_ans}"
                else:
                    covered = []
                    missed = []
                    for kw in kws:
                        if kw.lower() in user_ans.lower():
                            covered.append(kw)
                        else:
                            missed.append(kw)
                            
                    total_kws = len(kws)
                    pct = len(covered) / total_kws if total_kws > 0 else 1.0
                    score = round(45.0 + (pct * 45.0) + random.uniform(0, 5), 1)
                    if score > 100.0:
                        score = 100.0
                        
                    if covered:
                        feedback_critique = f"You did a good job explaining: {', '.join(covered)}."
                    else:
                        feedback_critique = "Your answer was too brief or did not address the core concepts required for this question."
                        
                    if not missed:
                        feedback_improvement = "Excellent answer! You covered all the key aspects of the question."
                    else:
                        feedback_improvement = f"To improve, you should also cover: {', '.join(missed)}. For a perfect score, your answer could be structured like: {ideal_ans}"
                
                feedback = f"Critique: {feedback_critique}\n\nHow to Improve: {feedback_improvement}\n\nIdeal Answer: {ideal_ans}"
                
                if score >= 80:
                    strengths_list.append(f"Strong understanding of {topic_name}.")
                else:
                    weaknesses_list.append(f"Needs to review core details of {topic_name}.")
                    recommendations_list.append(f"Practice explaining {topic_name} using the key terms: {', '.join(kws)}.")
                
                question_scores.append({
                    "question_id": q.id,
                    "score": score,
                    "feedback": feedback,
                    "feedback_critique": feedback_critique,
                    "feedback_improvement": feedback_improvement
                })
                total_score += score
                
            overall_score = round(total_score / len(questions), 2) if questions else 0.0
            
            # De-duplicate
            strengths_list = list(dict.fromkeys(strengths_list))
            weaknesses_list = list(dict.fromkeys(weaknesses_list))
            recommendations_list = list(dict.fromkeys(recommendations_list))
            
            if not strengths_list:
                strengths_list = [f"Completed the mock interview in {domain} successfully."]
            if not weaknesses_list:
                weaknesses_list = ["No significant weaknesses identified! Excellent work."]
            if not recommendations_list:
                recommendations_list = ["Keep practicing and study the ideal answer syntax."]
                
            return {
                "overall_score": overall_score,
                "strengths": strengths_list[:5],
                "weaknesses": weaknesses_list[:5],
                "recommendations": recommendations_list[:5],
                "question_scores": question_scores
            }
        
        try:
            overall_score = float(data.get("overall_score", 0))
        except (ValueError, TypeError):
            overall_score = 0.0
            
        strengths = self._string_list(data.get("strengths"))
        weaknesses = self._string_list(data.get("weaknesses"))
        recommendations = self._string_list(data.get("recommendations"))
        
        question_scores = []
        raw_scores = data.get("question_scores", [])
        if isinstance(raw_scores, list):
            for item in raw_scores:
                if isinstance(item, dict):
                    try:
                        q_id = int(item.get("question_id", 0))
                        score = float(item.get("score", 0))
                    except (ValueError, TypeError):
                        q_id = 0
                        score = 0.0
                        
                    critique = str(item.get("feedback_critique", "No critique provided."))
                    improvement = str(item.get("feedback_improvement", "No improvement details provided."))
                    
                    # Find the matching ideal answer from database to append
                    ideal_ans = "No ideal answer available."
                    for q in questions:
                        if q.id == q_id:
                            ideal_ans = q.ideal_answer or "No ideal answer available."
                            break
                            
                    feedback = f"Critique: {critique}\n\nHow to Improve: {improvement}\n\nIdeal Answer: {ideal_ans}"
                    
                    question_scores.append({
                        "question_id": q_id,
                        "score": score,
                        "feedback": feedback,
                        "feedback_critique": critique,
                        "feedback_improvement": improvement
                    })
                    
        return {
            "overall_score": overall_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "question_scores": question_scores
        }

    def _json_response(self, prompt: str) -> dict:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            text = (response.text or "").strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return {}
            
        if text.startswith("```"):
            text = text.strip("`")
            text = text.removeprefix("json").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {}

    def _fallback_questions(self, domain: str, total_questions: int) -> list[dict]:
        domain_qs = PREDEFINED_QUESTIONS.get(domain, [])
        if not domain_qs:
            domain_qs = [{
                "question_text": f"Explain an important {domain} concept and how you have applied it.",
                "ideal_answer": f"A comprehensive explanation of key {domain} concepts, their real-world application, trade-offs, and best practices.",
                "keywords": ["concept", "apply", "benefit"],
                "topic": f"{domain} General Concepts"
            }]
            
        if len(domain_qs) >= total_questions:
            selected = random.sample(domain_qs, total_questions)
        else:
            selected = []
            for i in range(total_questions):
                selected.append(domain_qs[i % len(domain_qs)])
            random.shuffle(selected)
            
        return [
            {
                "question_text": q["question_text"],
                "ideal_answer": q["ideal_answer"],
                "keywords": q["keywords"]
            }
            for q in selected
        ]

    def _string_list(self, value) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str) and value:
            return [value]
        return []
