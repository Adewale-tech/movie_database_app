import os
import sys
import dj_database_url
import psycopg2

def check_environment():
    print("--- Environment Check ---")
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL is NOT set in environment variables.")
        return False
    
    print("✅ DATABASE_URL is set.")
    # Mask the password for display
    safe_url = db_url.split('@')[-1] if '@' in db_url else '***'
    print(f"   Value (masked): ...{safe_url}")
    return db_url

def check_parsing(db_url):
    print("\n--- Parsing Check ---")
    try:
        config = dj_database_url.parse(db_url, conn_max_age=600, ssl_require=True)
        print("✅ dj_database_url parsed the URL successfully.")
        print(f"   Engine: {config.get('ENGINE')}")
        print(f"   Name: {config.get('NAME')}")
        print(f"   Host: {config.get('HOST')}")
        return config
    except Exception as e:
        print(f"❌ dj_database_url failed to parse URL: {e}")
        return None

def check_connection(config):
    print("\n--- Connection Check ---")
    try:
        conn = psycopg2.connect(
            dbname=config['NAME'],
            user=config['USER'],
            password=config['PASSWORD'],
            host=config['HOST'],
            port=config['PORT'],
            sslmode='require'
        )
        print("✅ Successfully connected to PostgreSQL!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    print("Starting Heroku Database Diagnostic...")
    db_url = check_environment()
    
    if db_url:
        config = check_parsing(db_url)
        if config:
            check_connection(config)
    
    print("\n--- End of Diagnostic ---")
