import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from dotenv import load_dotenv
import os
load_dotenv()

class LinkedInJobScraper:
    def __init__(self, email, password):
        """Initialize the scraper with LinkedIn credentials."""
        self.email = email
        self.password = password
        self.driver = None

    def setup_driver(self):
        """Set up Chrome WebDriver with necessary options."""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        """Log into LinkedIn."""
        self.driver.get('https://www.linkedin.com/login')
        
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(self.email)
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(self.password)
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        time.sleep(3)

    def _get_apply_link(self):
        """Extract the apply button link and metadata."""
        try:
            # Wait for the apply button to be present
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-button--top-card"))
            )
            
            # Get the apply button attributes
            apply_data = {
                'button_text': apply_button.text.strip(),
                'aria_label': apply_button.get_attribute('aria-label'),
                'apply_link': None
            }

         
            apply_link = apply_button.get_attribute('href')
            if not apply_link:
               
                apply_link = apply_button.get_attribute('data-live-test-job-apply-button')
            
            apply_data['apply_link'] = apply_link
            return apply_data
        except:
            return None

    def _get_save_button_info(self):
        """Extract the save button information."""
        try:
            save_button = self.driver.find_element(By.CLASS_NAME, "jobs-save-button")
            return {
                'button_text': save_button.text.strip(),
                'save_link': save_button.get_attribute('href'),
                'job_id': save_button.get_attribute('data-job-id')
            }
        except:
            return None

    def scrape_job_posting(self, job_url):
        """Scrape details from a LinkedIn job posting."""
        try:
            self.driver.get(job_url)
            
            # Wait for main job container to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-s-apply"))
            )
            
            # Extract job details
            job_data = {
                'job_url': job_url,
                'title': self._get_text_by_selector('.job-details-jobs-unified-top-card__job-title'),
                'company': self._get_text_by_selector('.job-details-jobs-unified-top-card__company-name'),
                'company_link': self._get_attribute_by_selector('.job-details-jobs-unified-top-card__company-name a', 'href'),
                'location': self._get_text_by_selector('.job-details-jobs-unified-top-card__bullet'),
                
                # Apply and Save button information
                'apply_info': self._get_apply_link(),
                'save_info': self._get_save_button_info(),
                
                # Description section
                'description': self._get_job_description(),
                'requirements': self._get_requirements(),
                
                # Additional details
                'job_info': self._get_job_info(),
                'applicant_info': self._get_applicant_info()
            }
            
            return job_data
            
        except TimeoutException:
            return {"error": "Failed to load job posting"}
        except Exception as e:
            return {"error": str(e)}

    def _get_text_by_selector(self, selector):
        """Get text using CSS selector."""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except:
            return None

    def _get_attribute_by_selector(self, selector, attribute):
        """Get attribute value using CSS selector."""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.get_attribute(attribute)
        except:
            return None

    def _get_job_description(self):
        """Extract job description."""
        try:
            description_container = self.driver.find_element(By.CLASS_NAME, 
                "jobs-description__content")
            return description_container.text.strip()
        except:
            return None

    def _get_requirements(self):
        """Extract requirements from the job description."""
        requirements = []
        try:
            job_details = self.driver.find_element(By.ID, "job-details")
            content = job_details.get_attribute('innerHTML')
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find the "Key Responsibilities" heading and get the following list items
            for strong_tag in soup.find_all('strong'):
                if 'Key Responsibilities' in strong_tag.text:
                    current = strong_tag.parent
                    while current:
                        if current.name == 'li' or (current.name == 'p' and '•' in current.text):
                            requirements.append(current.text.strip())
                        current = current.next_sibling
        except:
            pass
        return requirements

    def _get_job_info(self):
        """Extract job information."""
        try:
            info_container = self.driver.find_element(By.CLASS_NAME, 
                "job-details-jobs-unified-top-card__primary-description-container")
            return info_container.text.strip()
        except:
            return None

    def _get_applicant_info(self):
        """Extract applicant information."""
        try:
            applicant_container = self.driver.find_element(By.CLASS_NAME,
                "job-details-jobs-unified-top-card__top-buttons")
            return applicant_container.text.strip()
        except:
            return None

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
def save_jobs_to_json(jobs_data, filename='linkedin_jobs.json'):
    """Save scraped jobs data to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(jobs_data, json_file, indent=2)

def scrape_linkedin_job(job_urls, linkedin_email, linkedin_password):
    """Main function to scrape a LinkedIn job posting."""
    scraper = LinkedInJobScraper(linkedin_email, linkedin_password)
    
    try:
        jobs_data =[]
        scraper.setup_driver()
        scraper.login()
        for job_url in job_urls:
            job_data = scraper.scrape_job_posting(job_url)
            jobs_data.append(json.dumps(job_data, indent=2))
        
        return jobs_data
    finally:
        scraper.close()
# Example usage
if __name__ == "__main__":
    job_urls = ["https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4063006968"]
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    
    job_details = scrape_linkedin_job(job_urls, linkedin_email, linkedin_password)
    save_jobs_to_json(job_details)
    print(job_details)