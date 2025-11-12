"""
דוגמאות שימוש בבוט Code to Image
===================================

קובץ זה מכיל דוגמאות לקטעי קוד שניתן לשלוח לבוט לבדיקה
"""

# ============================================
# דוגמה 1: Python - פונקציה פשוטה
# ============================================

def greet(name):
    """Greet someone by name"""
    return f"Hello, {name}!"

# ============================================
# דוגמה 2: Python - קלאס
# ============================================

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        self.result = x + y
        return self.result
    
    def multiply(self, x, y):
        self.result = x * y
        return self.result

# ============================================
# דוגמה 3: JavaScript - פונקציית חץ
# ============================================

const fibonacci = (n) => {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
};

console.log(fibonacci(10));

# ============================================
# דוגמה 4: JavaScript - Async/Await
# ============================================

async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching user:', error);
    }
}

# ============================================
# דוגמה 5: TypeScript - Interface
# ============================================

interface User {
    id: number;
    name: string;
    email: string;
    isActive: boolean;
}

function getUserInfo(user: User): string {
    return `${user.name} (${user.email})`;
}

# ============================================
# דוגמה 6: Python - List Comprehension
# ============================================

numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers if x % 2 == 0]
print(squares)  # [4, 16]

# ============================================
# דוגמה 7: SQL Query
# ============================================

SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.username
HAVING COUNT(p.id) > 5
ORDER BY post_count DESC;

# ============================================
# דוגמה 8: HTML/CSS
# ============================================

<!DOCTYPE html>
<html>
<head>
    <style>
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome!</h1>
    </div>
</body>
</html>

# ============================================
# דוגמה 9: Go - Goroutines
# ============================================

package main

import (
    "fmt"
    "time"
)

func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, j)
        time.Sleep(time.Second)
        results <- j * 2
    }
}

# ============================================
# דוגמה 10: Rust - Pattern Matching
# ============================================

fn describe_number(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1..=10 => "small",
        11..=100 => "medium",
        _ => "large",
    }
}

fn main() {
    println!("{}", describe_number(5));
}

# ============================================
# דוגמה 11: Python - Decorator
# ============================================

import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    return "Done!"

# ============================================
# דוגמה 12: React Component
# ============================================

import React, { useState, useEffect } from 'react';

const UserProfile = ({ userId }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(data => {
                setUser(data);
                setLoading(false);
            });
    }, [userId]);
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div className="profile">
            <h2>{user.name}</h2>
            <p>{user.email}</p>
        </div>
    );
};

# ============================================
# הוראות שימוש:
# ============================================
"""
1. העתק אחת מהדוגמאות למעלה
2. שלח אותה לבוט בטלגרם
3. הבוט יזהה אוטומטית את השפה ויצור תמונה מעוצבת
4. אפשר לשנות ערכת נושא דרך /theme
5. אפשר לבחור שפה ידנית דרך /language

טיפים:
- אם שולחים קוד עם ```, הבוט יזהה את השפה אוטומטית
- ניתן לכלול מספר שורות
- הבוט תומך במגוון רחב של שפות תכנות
- כל ההגדרות נשמרות אוטומטית
"""
