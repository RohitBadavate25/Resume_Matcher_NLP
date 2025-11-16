import requests
import json

def test_matching_api():
    """Test the matching API to see if it's working correctly"""
    
    # Get job descriptions first
    print("🔍 Getting job descriptions...")
    jobs_response = requests.get('http://127.0.0.1:5000/api/job-descriptions')
    
    if jobs_response.status_code == 200:
        response_data = jobs_response.json()
        jobs_data = response_data.get('job_descriptions', []) if isinstance(response_data, dict) else response_data
        print(f"✅ Found {len(jobs_data)} job descriptions")
        print(f"Full response: {response_data}")
        
        if jobs_data:
            # Use the first job for testing
            test_job_id = jobs_data[0]['id']
            job_title = jobs_data[0]['title']
            print(f"📋 Testing with job: {job_title} (ID: {test_job_id})")
            
            # Test matching
            print("\n🎯 Running matching...")
            match_response = requests.post('http://127.0.0.1:5000/api/match', 
                                         json={'job_id': test_job_id})
            
            if match_response.status_code == 200:
                match_data = match_response.json()
                print(f"✅ Matching successful!")
                print(f"📊 Total candidates: {match_data.get('total_candidates', 0)}")
                
                matches = match_data.get('matches', [])
                print(f"\n🏆 Top matches:")
                
                for i, match in enumerate(matches[:3], 1):
                    name = match.get('candidate_name', 'Unknown')
                    similarity = match.get('match_percentage', 0)
                    strength = match.get('match_category', 'Unknown')
                    
                    print(f"  {i}. {name}: {similarity}% ({strength})")
                    
                    # Show component breakdown
                    components = match.get('component_scores', {})
                    if components:
                        print(f"     TF-IDF: {components.get('tfidf_similarity', 0):.3f}")
                        print(f"     Skills: {components.get('skill_similarity', 0):.3f}")
                        print(f"     Semantic: {components.get('semantic_similarity', 0):.3f}")
                
                # Check if we're getting non-zero results
                non_zero_matches = [m for m in matches if m.get('match_percentage', 0) > 0]
                if non_zero_matches:
                    print(f"\n✅ SUCCESS: {len(non_zero_matches)} candidates have non-zero matches!")
                else:
                    print(f"\n❌ PROBLEM: All matches are 0%")
                    
            else:
                print(f"❌ Matching failed: {match_response.status_code}")
                print(match_response.text)
        else:
            print("❌ No job descriptions found in database")
    else:
        print(f"❌ Failed to get job descriptions: {jobs_response.status_code}")

if __name__ == "__main__":
    test_matching_api()