"""
LinkedIn Profile Query Processor

This module processes natural language queries about LinkedIn profiles
and extracts relevant information from stored profile data.
"""

import re
import json
import os
from typing import Dict, List, Any, Optional, Tuple
import spacy

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_md")
except:
    # If the model isn't installed, use a smaller model
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        print("Please install spaCy models: python -m spacy download en_core_web_sm")
        raise

class ProfileQueryProcessor:
    def __init__(self, profiles_dir: str = "profiles"):
        """
        Initialize the profile query processor.
        
        Args:
            profiles_dir: Directory containing profile data
        """
        self.profiles_dir = profiles_dir
        self.loaded_profiles = {}
        self._load_all_profiles()
        
        # Define query categories and their related keywords
        self.query_categories = {
            "education": ["education", "degree", "university", "college", "school", 
                         "study", "studied", "graduate", "graduated", "qualification",
                         "academic", "diploma", "bachelor", "master", "phd", "doctorate"],
            
            "experience": ["experience", "work", "job", "position", "employment", "career",
                          "company", "organization", "industry", "role", "worked", 
                          "working", "professional"],
            
            "skills": ["skill", "expertise", "proficiency", "capability", "competency", 
                      "talent", "ability", "know", "knows", "proficient", "capable",
                      "experienced in"],
            
            "languages": ["language", "speak", "speaking", "fluent", "proficient", 
                         "native", "bilingual", "multilingual"],
            
            "certifications": ["certification", "certificate", "certified", "credential", 
                              "qualification", "license", "accreditation"],
            
            "location": ["location", "located", "live", "lives", "based", "residing", 
                        "residence", "city", "country", "address", "area"],
            
            "contact": ["contact", "email", "phone", "website", "connect", "reach", 
                       "social media", "linkedin", "twitter"],
            
            "general": ["about", "profile", "background", "summary", "overview", 
                       "introduction", "who is", "tell me about", "information"]
        }
    
    def _load_all_profiles(self) -> None:
        """Load all available profiles from the profiles directory."""
        if not os.path.exists(self.profiles_dir):
            print(f"Profiles directory {self.profiles_dir} does not exist.")
            return
        
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith(".json"):
                profile_id = filename[:-5]  # Remove .json extension
                self._load_profile(profile_id)
    
    def _load_profile(self, profile_id: str) -> bool:
        """
        Load a specific profile by ID.
        
        Args:
            profile_id: Profile identifier
        
        Returns:
            True if profile was loaded successfully, False otherwise
        """
        filename = os.path.join(self.profiles_dir, f"{profile_id}.json")
        
        if not os.path.exists(filename):
            return False
        
        with open(filename, "r") as f:
            self.loaded_profiles[profile_id] = json.load(f)
        
        return True
    
    def extract_profile_name_from_query(self, query: str) -> Optional[str]:
        """
        Extract profile name or ID from a query.
        
        Args:
            query: User query text
            
        Returns:
            Profile ID if found, None otherwise
        """
        # Process query with spaCy
        doc = nlp(query)
        
        # Look for entities that could be person names
        person_entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        
        if person_entities:
            # Try to match person names with our loaded profiles
            for person in person_entities:
                for profile_id, profile_data in self.loaded_profiles.items():
                    profile_name = profile_data["basics"]["name"]
                    if person.lower() in profile_name.lower():
                        return profile_id
            
            # If no exact match, look for partial matches
            best_match = None
            best_score = 0
            
            for person in person_entities:
                for profile_id, profile_data in self.loaded_profiles.items():
                    profile_name = profile_data["basics"]["name"]
                    # Simple string similarity - percentage of characters that match
                    similarity = len(set(person.lower()) & set(profile_name.lower())) / max(len(person), len(profile_name))
                    if similarity > 0.5 and similarity > best_score:
                        best_match = profile_id
                        best_score = similarity
            
            if best_match:
                return best_match
        
        # Try regex patterns for profile queries
        patterns = [
            r"(?:of|about|for)\s+([A-Za-z\s.'-]+?)(?:'s|\s+at|\s+from|\s+in|\s+who|\?|$)",
            r"([A-Za-z\s.'-]+?)(?:'s)\s+(?:education|experience|profile|background)"
        ]
        
        for pattern in patterns:
            matches = re.search(pattern, query, re.IGNORECASE)
            if matches:
                name = matches.group(1).strip()
                
                # Try to match this name against our profiles
                for profile_id, profile_data in self.loaded_profiles.items():
                    profile_name = profile_data["basics"]["name"]
                    if name.lower() in profile_name.lower() or profile_name.lower() in name.lower():
                        return profile_id
        
        # Direct check for profile IDs in the query
        for profile_id in self.loaded_profiles.keys():
            if profile_id.lower() in query.lower():
                return profile_id
        
        return None
    
    def identify_query_category(self, query: str) -> str:
        """
        Identify the category of information the query is asking about.
        
        Args:
            query: User query text
            
        Returns:
            Category name (education, experience, skills, etc.)
        """
        query_lower = query.lower()
        
        # Check each category's keywords
        max_matches = 0
        best_category = "general"  # Default category
        
        for category, keywords in self.query_categories.items():
            matches = sum(keyword in query_lower for keyword in keywords)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        return best_category
    
    def extract_specific_request(self, query: str, category: str) -> Optional[str]:
        """
        Extract specific details about what's being requested.
        
        Args:
            query: User query text
            category: Query category
            
        Returns:
            Specific request detail if found, None otherwise
        """
        # This function would implement more sophisticated extraction
        # For now, we'll return a simplified approach
        
        if category == "experience":
            for keyword in ["current", "latest", "most recent"]:
                if keyword in query.lower():
                    return "current"
                
            for keyword in ["previous", "past", "before", "former"]:
                if keyword in query.lower():
                    return "previous"
                
            # Check for specific company mentions
            doc = nlp(query)
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    return f"company:{ent.text}"
        
        elif category == "education":
            for keyword in ["highest", "latest", "most recent"]:
                if keyword in query.lower():
                    return "highest"
            
            for degree in ["bachelor", "master", "phd", "doctorate", "mba"]:
                if degree in query.lower():
                    return f"degree:{degree}"
        
        return None
    
    def process_query(self, query: str) -> Dict:
        """
        Process a natural language query about a LinkedIn profile.
        
        Args:
            query: User query text
            
        Returns:
            Dictionary with query analysis and response
        """
        # Extract profile ID from query
        profile_id = self.extract_profile_name_from_query(query)
        
        if not profile_id:
            return {
                "success": False,
                "error": "Could not identify a profile in your query",
                "available_profiles": list(self.loaded_profiles.keys())
            }
        
        # Make sure profile is loaded
        if profile_id not in self.loaded_profiles:
            success = self._load_profile(profile_id)
            if not success:
                return {
                    "success": False,
                    "error": f"Profile {profile_id} not found",
                    "available_profiles": list(self.loaded_profiles.keys())
                }
        
        profile_data = self.loaded_profiles[profile_id]
        
        # Identify query category
        category = self.identify_query_category(query)
        
        # Extract specific request details
        specific_request = self.extract_specific_request(query, category)
        
        # Generate response based on category and profile data
        response = self._generate_response(profile_data, category, specific_request)
        
        return {
            "success": True,
            "profile_id": profile_id,
            "category": category,
            "specific_request": specific_request,
            "response": response
        }
    
    def _generate_response(self, profile: Dict, category: str, specific_request: Optional[str] = None) -> str:
        """
        Generate a response based on profile data and query category.
        
        Args:
            profile: Profile data dictionary
            category: Query category
            specific_request: Specific request details
            
        Returns:
            Response text
        """
        profile_name = profile["basics"]["name"]
        
        if category == "education":
            if not profile.get("education"):
                return f"{profile_name} has no education information in their profile."
            
            if specific_request == "highest":
                # Assuming education is listed in reverse chronological order
                highest_edu = profile["education"][0]
                return f"{profile_name}'s highest education is {highest_edu['degree']} from {highest_edu['institution']} ({highest_edu['date_range']})."
            
            # If looking for a specific degree
            if specific_request and specific_request.startswith("degree:"):
                degree_type = specific_request.split(":", 1)[1]
                matching_degrees = [edu for edu in profile["education"] 
                                   if degree_type.lower() in edu["degree"].lower()]
                
                if matching_degrees:
                    edu = matching_degrees[0]
                    return f"{profile_name} has a {edu['degree']} from {edu['institution']} ({edu['date_range']})."
                else:
                    return f"Could not find a {degree_type} degree for {profile_name}."
            
            # Default: list all education
            edu_list = [f"{edu['degree']} from {edu['institution']} ({edu['date_range']})" 
                        for edu in profile["education"]]
            return f"{profile_name}'s education: {'; '.join(edu_list)}."
        
        elif category == "experience":
            if not profile.get("experience"):
                return f"{profile_name} has no work experience information in their profile."
            
            if specific_request == "current":
                # Assuming experience is listed in reverse chronological order
                current_job = profile["experience"][0]
                return f"{profile_name} currently works as {current_job['title']} at {current_job['company']} ({current_job['duration']})."
            
            if specific_request == "previous":
                if len(profile["experience"]) > 1:
                    prev_job = profile["experience"][1]
                    return f"{profile_name} previously worked as {prev_job['title']} at {prev_job['company']} ({prev_job['duration']})."
                else:
                    return f"No previous job experience found for {profile_name} before their current role."
            
            # If looking for experience at a specific company
            if specific_request and specific_request.startswith("company:"):
                company_name = specific_request.split(":", 1)[1]
                matching_jobs = [job for job in profile["experience"] 
                                if company_name.lower() in job["company"].lower()]
                
                if matching_jobs:
                    job = matching_jobs[0]
                    return f"{profile_name} worked as {job['title']} at {job['company']} ({job['duration']})."
                else:
                    return f"Could not find experience at {company_name} for {profile_name}."
            
            # Default: list all experience
            exp_list = [f"{job['title']} at {job['company']} ({job['duration']})" 
                       for job in profile["experience"]]
            return f"{profile_name}'s work experience: {'; '.join(exp_list)}."
        
        elif category == "skills":
            if not profile.get("skills"):
                return f"{profile_name} has no skills listed in their profile."
            
            return f"{profile_name}'s skills include: {', '.join(profile['skills'])}."
        
        elif category == "languages":
            if not profile.get("languages"):
                return f"{profile_name} has no language information in their profile."
            
            lang_list = [f"{lang['language']} ({lang['proficiency']})" for lang in profile["languages"]]
            return f"{profile_name} speaks: {', '.join(lang_list)}."
        
        elif category == "certifications":
            if not profile.get("certifications"):
                return f"{profile_name} has no certifications listed in their profile."
            
            cert_list = [f"{cert['name']} from {cert['issuer']} ({cert['date']})" 
                        for cert in profile["certifications"]]
            return f"{profile_name}'s certifications: {'; '.join(cert_list)}."
        
        elif category == "location":
            location = profile["basics"].get("location", "Unknown")
            return f"{profile_name} is located in {location}."
        
        elif category == "contact":
            if not profile.get("contact_info"):
                return f"No contact information available for {profile_name}."
            
            contact_info = profile["contact_info"]
            return f"Contact information for {profile_name}: Email: {contact_info.get('email', 'Not provided')}, Phone: {contact_info.get('phone', 'Not provided')}."
        
        else:  # General information
            basics = profile["basics"]
            summary = [
                f"{profile_name} is a {basics.get('headline', 'professional')}",
                f"based in {basics.get('location', 'an unknown location')}."
            ]
            
            if basics.get("summary"):
                summary.append(f"Summary: {basics['summary']}")
            
            if profile.get("experience") and len(profile["experience"]) > 0:
                current_job = profile["experience"][0]
                summary.append(f"Currently working as {current_job['title']} at {current_job['company']}.")
            
            if profile.get("education") and len(profile["education"]) > 0:
                highest_edu = profile["education"][0]
                summary.append(f"Has studied {highest_edu['degree']} at {highest_edu['institution']}.")
            
            return " ".join(summary)

# Example usage
if __name__ == "__main__":
    # Create processor instance
    processor = ProfileQueryProcessor()
    
    # Example queries
    test_queries = [
        "What is the educational qualification of Example User?",
        "Where did Example User study?",
        "What is Example User's current job?",
        "Tell me about Example User's work experience at Tech Corp",
        "What skills does Example User have?",
        "Does Example User speak Spanish?",
        "Where is Example User located?",
        "Tell me about Example User's certifications",
        "How can I contact Example User?",
        "Tell me about Example User"
    ]
    
    # Process each query
    for query in test_queries:
        print("\nQuery:", query)
        result = processor.process_query(query)
        
        if result["success"]:
            print("Response:", result["response"])
            print("Category:", result["category"])
        else:
            print("Error:", result["error"])
