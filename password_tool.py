# ============================================
# PASSWORD STRENGTH ANALYZER & HASH CRACKER
# Student: Karima
# Roll Number: Bitf23m053
# Date: 28 Feb 2026
# ============================================

import hashlib
import time
import string
import itertools
import os
import sys

# ========== PART 1: PASSWORD STRENGTH CHECKER ==========

def check_password_strength(password):
    """
    Analyzes password strength and returns score, strength label, and feedback
    """
    score = 0
    feedback = []
    
    # 1. Length check (max 35 points)
    length = len(password)
    if length >= 14:
        score += 35
        feedback.append(f"✓ Length: {length} characters (Excellent!)")
    elif length >= 10:
        score += 25
        feedback.append(f"✓ Length: {length} characters (Good)")
    elif length >= 8:
        score += 15
        feedback.append(f"⚠ Length: {length} characters (Minimum met, but 12+ is better)")
    elif length > 0:
        score += 5
        feedback.append(f"✗ Length: {length} characters (Need at least 8 characters)")
    
    # 2. Character variety (max 45 points)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/~`" for c in password)
    
    if has_upper:
        score += 11
        feedback.append("✓ Contains uppercase letters (A-Z)")
    else:
        feedback.append("✗ Missing uppercase letters - Add A-Z")
        
    if has_lower:
        score += 11
        feedback.append("✓ Contains lowercase letters (a-z)")
    else:
        feedback.append("✗ Missing lowercase letters - Add a-z")
        
    if has_digit:
        score += 11
        feedback.append("✓ Contains numbers (0-9)")
    else:
        feedback.append("✗ Missing numbers - Add 0-9")
        
    if has_special:
        score += 12
        feedback.append("✓ Contains special characters (!@#$%)")
    else:
        feedback.append("✗ Missing special characters - Add !@#$%")
    
    # 3. Common password detection (penalty)
    common_passwords = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "admin", "letmein", "welcome", "monkey", "dragon",
        "password123", "admin123", "iloveyou", "sunshine", "football"
    ]
    
    if password.lower() in common_passwords:
        score = max(0, score - 40)
        feedback.append("⚠ WARNING: This is a commonly used weak password!")
    
    # 4. Sequential patterns (penalty)
    sequences = ["1234", "2345", "3456", "4567", "5678", "6789",
                 "abcd", "bcde", "cdef", "defg", "qwert", "asdf", "zxcv"]
    
    for seq in sequences:
        if seq in password.lower():
            score = max(0, score - 25)
            feedback.append(f"⚠ Contains sequential pattern '{seq}' (easily guessable)")
            break
    
    # 5. Repetitive characters (penalty)
    if len(set(password)) <= 3:
        score = max(0, score - 30)
        feedback.append("⚠ Too many repeated characters!")
    
    # Determine strength level
    if score >= 75:
        strength = "STRONG 💪"
        emoji = "🟢"
    elif score >= 45:
        strength = "MEDIUM 👍"
        emoji = "🟡"
    else:
        strength = "WEAK ⚠"
        emoji = "🔴"
    
    return score, strength, feedback, emoji

# ========== PART 2: HASH GENERATOR ==========

def generate_hash(password, hash_type="md5"):
    """Convert password to hash"""
    if hash_type == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif hash_type == "sha1":
        return hashlib.sha1(password.encode()).hexdigest()
    else:
        return None

# ========== PART 3: DICTIONARY ATTACK ==========

def dictionary_attack(target_hash, hash_type="md5"):
    """Simulate dictionary attack with common passwords"""
    
    common_passwords = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "admin", "letmein", "welcome", "monkey", "dragon",
        "password123", "admin123", "iloveyou", "sunshine",
        "football", "baseball", "master", "hello", "robert",
        "starwars", "computer", "internet", "whatever", "trustno1"
    ]
    
    print(f"\n[*] Starting Dictionary Attack on {hash_type.upper()} hash...")
    print(f"[*] Testing {len(common_passwords)} common passwords...")
    print("-" * 40)
    
    start_time = time.time()
    
    for idx, password in enumerate(common_passwords, 1):
        # Show progress
        print(f"  Trying [{idx}/{len(common_passwords)}]: {password}", end="\r")
        
        test_hash = generate_hash(password, hash_type)
        
        if test_hash == target_hash:
            elapsed = time.time() - start_time
            print(f"\n\n{'='*40}")
            print(f"✓✓✓ PASSWORD CRACKED! ✓✓✓")
            print(f"{'='*40}")
            print(f"  Password: {password}")
            print(f"  Time: {elapsed:.2f} seconds")
            print(f"  Attempts: {idx}")
            return True, password
    
    elapsed = time.time() - start_time
    print(f"\n\n{'='*40}")
    print(f"✗ Dictionary Attack Failed")
    print(f"{'='*40}")
    print(f"  Password not in common password list")
    print(f"  Time: {elapsed:.2f} seconds")
    print(f"  Attempts tested: {len(common_passwords)}")
    return False, None

# ========== PART 4: BRUTE FORCE DEMO ==========

def brute_force_demo(target_hash, max_length=4, hash_type="md5"):
    """Demonstrate brute force attack (limited to 4 chars for speed)"""
    
    characters = string.ascii_lowercase + string.digits  # a-z and 0-9
    total_combinations = sum(len(characters)**i for i in range(1, max_length+1))
    
    print(f"\n[*] Starting Brute-Force Attack")
    print(f"[*] Max length: {max_length} characters")
    print(f"[*] Character set: a-z, 0-9 ({len(characters)} chars)")
    print(f"[*] Max combinations: {total_combinations:,}")
    print("-" * 40)
    
    start_time = time.time()
    attempts = 0
    
    for length in range(1, max_length + 1):
        print(f"\n[*] Trying passwords of length {length}...")
        
        for combo in itertools.product(characters, repeat=length):
            password = ''.join(combo)
            attempts += 1
            
            # Show progress every 5000 attempts
            if attempts % 5000 == 0:
                print(f"     Attempts: {attempts:,}... Current: {password}", end="\r")
            
            test_hash = generate_hash(password, hash_type)
            
            if test_hash == target_hash:
                elapsed = time.time() - start_time
                print(f"\n\n{'='*40}")
                print(f"✓✓✓ PASSWORD CRACKED! ✓✓✓")
                print(f"{'='*40}")
                print(f"  Password: {password}")
                print(f"  Time: {elapsed:.2f} seconds")
                print(f"  Attempts: {attempts:,}")
                return True, password
    
    elapsed = time.time() - start_time
    print(f"\n\n{'='*40}")
    print(f"✗ Brute-Force Failed")
    print(f"{'='*40}")
    print(f"  Password longer than {max_length} characters")
    print(f"  Time: {elapsed:.2f} seconds")
    print(f"  Attempts: {attempts:,}")
    return False, None

# ========== PART 5: TIME ESTIMATION ==========

def estimate_crack_time(password):
    """Estimate how long it would take to crack the password"""
    
    length = len(password)
    char_set_size = 0
    
    if any(c.islower() for c in password):
        char_set_size += 26
    if any(c.isupper() for c in password):
        char_set_size += 26
    if any(c.isdigit() for c in password):
        char_set_size += 10
    if any(c in "!@#$%^&*()" for c in password):
        char_set_size += 32
    
    if char_set_size == 0:
        char_set_size = 26
    
    combinations = char_set_size ** length
    
    # Different attack speeds (guesses per second)
    online_attack = 1000      # Slow - online service
    offline_md5 = 10000000000  # Fast - 10 billion/sec
    offline_bcrypt = 10000     # Slow - bcrypt
    
    online_time = combinations / online_attack
    md5_time = combinations / offline_md5
    bcrypt_time = combinations / offline_bcrypt
    
    return {
        "online": online_time,
        "md5": md5_time,
        "bcrypt": bcrypt_time,
        "combinations": combinations,
        "char_set": char_set_size
    }

def format_time(seconds):
    """Convert seconds to readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    else:
        return f"{seconds/31536000:.1f} years"

# ========== PART 6: VISUAL PROGRESS BAR ==========

def show_progress_bar(percentage, width=30):
    """Display a colored progress bar"""
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    
    if percentage < 40:
        return f"\033[91m[{bar}] {percentage}%\033[0m"  # Red
    elif percentage < 70:
        return f"\033[93m[{bar}] {percentage}%\033[0m"  # Yellow
    else:
        return f"\033[92m[{bar}] {percentage}%\033[0m"  # Green

# ========== MAIN MENU ==========

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main program loop"""
    
    while True:
        clear_screen()
        
        print("=" * 60)
        print("    PASSWORD STRENGTH ANALYZER & HASH CRACKER")
        print("=" * 60)
       # print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. 🔐 Password Strength Analyzer")
        print("2. 🔓 Password Cracking Simulator")
        print("3. 📊 Password Generator")
        print("4. ❌ Exit")
        print("-" * 60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        # Option 1: Password Strength Analyzer
        if choice == "1":
            clear_screen()
            print("=" * 60)
            print("    PASSWORD STRENGTH ANALYZER")
            print("=" * 60)
            
            password = input("\nEnter password to analyze: ")
            
            if len(password) == 0:
                print("\nNo password entered!")
                input("\nPress Enter to continue...")
                continue
            
            # Analyze password
            score, strength, feedback, emoji = check_password_strength(password)
            
            # Display results
            print("\n" + "=" * 60)
            print("RESULTS")
            print("=" * 60)
            print(f"\nPassword: {'*' * len(password)}")
            print(f"Length: {len(password)} characters")
            print(f"\nScore: {score}/100")
            print(f"Rating: {emoji} {strength}")
            
            # Show progress bar
            print(f"\nStrength Meter: {show_progress_bar(score)}")
            
            print("\n" + "-" * 40)
            print("DETAILED FEEDBACK:")
            print("-" * 40)
            for msg in feedback:
                print(f"  {msg}")
            
            # Show hash values
            print("\n" + "-" * 40)
            print("HASH VALUES (for this password):")
            print("-" * 40)
            print(f"MD5:  {generate_hash(password, 'md5')}")
            print(f"SHA-1: {generate_hash(password, 'sha1')}")
            
            # Show crack time estimates
            estimates = estimate_crack_time(password)
            print("\n" + "-" * 40)
            print("CRACKING TIME ESTIMATES:")
            print("-" * 40)
            print(f"Character set size: {estimates['char_set']} characters")
            print(f"Total combinations: {estimates['combinations']:,}")
            print(f"Online attack: {format_time(estimates['online'])}")
            print(f"MD5 hash (fast): {format_time(estimates['md5'])}")
            print(f"bcrypt hash (slow): {format_time(estimates['bcrypt'])}")
            
            input("\nPress Enter to continue...")
        
        # Option 2: Password Cracking Simulator
        elif choice == "2":
            clear_screen()
            print("=" * 60)
            print("    PASSWORD CRACKING SIMULATOR")
            print("=" * 60)
            print("\n⚠️  EDUCATIONAL DEMONSTRATION ONLY")
            print("This shows how hackers attempt to crack passwords")
            print("-" * 60)
            
            print("\nHow to proceed:")
            print("1. Enter a password to hash and crack")
            print("2. Enter a hash directly")
            
            crack_choice = input("\nChoice (1-2): ").strip()
            
            target_hash = None
            hash_type = "md5"
            original_password = None
            
            if crack_choice == "1":
                password = input("\nEnter password to crack: ")
                
                print("\nHash type:")
                print("1. MD5 (faster)")
                print("2. SHA-1")
                hash_choice = input("Choice (1-2): ").strip()
                hash_type = "md5" if hash_choice == "1" else "sha1"
                
                target_hash = generate_hash(password, hash_type)
                original_password = password
                print(f"\n[+] Generated {hash_type.upper()} hash: {target_hash}")
            
            elif crack_choice == "2":
                target_hash = input("\nEnter hash to crack: ").strip()
                print("\nHash type:")
                print("1. MD5")
                print("2. SHA-1")
                hash_choice = input("Choice (1-2): ").strip()
                hash_type = "md5" if hash_choice == "1" else "sha1"
            
            if target_hash:
                print("\n" + "-" * 40)
                print("CRACKING METHODS:")
                print("-" * 40)
                print("1. Dictionary Attack (fast)")
                print("2. Brute-Force Attack (thorough, max 4 chars)")
                print("3. Both methods")
                
                method = input("\nChoose method (1-3): ").strip()
                
                if method in ["1", "3"]:
                    dictionary_attack(target_hash, hash_type)
                
                if method in ["2", "3"]:
                    brute_force_demo(target_hash, max_length=4, hash_type=hash_type)
                
                if original_password:
                    print(f"\nOriginal password was: {original_password}")
            else:
                print("\nInvalid input!")
            
            input("\nPress Enter to continue...")
        
        # Option 3: Password Generator
        elif choice == "3":
            clear_screen()
            print("=" * 60)
            print("    PASSWORD GENERATOR")
            print("=" * 60)
            
            import random
            
            def generate_password(length=12, use_upper=True, use_lower=True, 
                                  use_digits=True, use_special=True):
                """Generate a random strong password"""
                chars = ""
                if use_upper:
                    chars += string.ascii_uppercase
                if use_lower:
                    chars += string.ascii_lowercase
                if use_digits:
                    chars += string.digits
                if use_special:
                    chars += "!@#$%^&*"
                
                if not chars:
                    chars = string.ascii_lowercase
                
                return ''.join(random.choice(chars) for _ in range(length))
            
            print("\nPassword Options:")
            print("-" * 40)
            
            try:
                length = int(input("Password length (8-20, default 12): ") or "12")
                length = max(8, min(20, length))
            except:
                length = 12
            
            print("\nInclude:")
            use_upper = input("Uppercase letters? (y/n, default y): ").lower() != 'n'
            use_lower = input("Lowercase letters? (y/n, default y): ").lower() != 'n'
            use_digits = input("Numbers? (y/n, default y): ").lower() != 'n'
            use_special = input("Special characters? (y/n, default y): ").lower() != 'n'
            
            # Generate multiple passwords
            print("\n" + "=" * 60)
            print("GENERATED PASSWORDS:")
            print("=" * 60)
            
            for i in range(5):
                password = generate_password(length, use_upper, use_lower, use_digits, use_special)
                score, strength, _, emoji = check_password_strength(password)
                print(f"\n{i+1}. {password}")
                print(f"   Strength: {emoji} {strength} ({score}/100)")
                print(f"   Hash MD5: {generate_hash(password, 'md5')[:16]}...")
            
            input("\nPress Enter to continue...")
        
        # Option 4: Exit
        elif choice == "4":
            clear_screen()
            print("\n" + "=" * 60)
            print("    THANK YOU FOR USING PASSWORD TOOL!")
            print("=" * 60)
            print("\n📌 Remember:")
            print("   • Use passwords at least 12 characters long")
            print("   • Mix uppercase, lowercase, numbers, and symbols")
            print("   • Never reuse passwords across different sites")
            print("   • Enable 2-factor authentication when available")
            print("\n🔐 Stay safe online!")
            print("=" * 60)
            break
        
        else:
            print("\nInvalid choice! Please enter 1, 2, 3, or 4.")
            time.sleep(1.5)

# Run the program
if __name__ == "__main__":
    main()