# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

SwagFinder2.0

---

## 2. Intended Use  

My recommender is designed to generate music recommendations based on a user’s preferred genre, mood, energy level, and acoustic style. It tries to suggest songs that match the user’s overall vibe rather than just one single feature.

It assumes the user can describe their taste with a few simple preferences, such as favorite genre, favorite mood, and target energy. It also assumes that songs with similar attributes are likely to appeal to the same listener.

This system is mainly for classroom exploration rather than real-world users. It is a simplified simulation that helps demonstrate how recommendation logic, scoring, and ranking work in practice.  

---

## 3. How the Model Works  

The model uses each song’s genre, mood, energy, and acousticness to decide how well it matches a user. Genre and mood are categorical features, while energy and acousticness help measure how close the song is to the user’s preferred vibe.

The user preferences considered are favorite genre, favorite mood, target energy, and whether the user likes acoustic songs. Together, these preferences act like a taste profile that the recommender compares against every song in the dataset.

The model turns those features into a score by giving points for matching genre and mood, then adding similarity points when a song’s energy is close to the user’s target. It can also give a small bonus when the user likes acoustic music and the song has high acousticness.

From the starter logic, I changed the system from placeholder behavior into a real scoring-based recommender. I implemented CSV loading, added weighted scoring rules with explanations, expanded the dataset, and tested how changing features like mood affected the rankings.

---

## 4. Data  

The dataset contains 20 songs in total and is stored in data/songs.csv. It includes a mix of genres and moods such as pop, lofi, rock, ambient, jazz, electronic, hip-hop, soul, country, classical, metal, reggae, blues, and folk, along with moods like happy, chill, intense, relaxed, moody, romantic, melancholic, contemplative, dark, and uplifting. I expanded the starter dataset by adding more songs so the catalog would be more diverse and better for testing different user profiles. Even with those additions, parts of musical taste are still missing, such as lyrics, personal listening history, artist relationships, and more detailed subgenres or emotional nuances. 

---

## 5. Strengths  

The system gives the most reasonable results for users with clear and consistent taste profiles, such as someone who likes high-energy pop, chill lofi, or intense rock. My scoring seems to capture the pattern that songs should match both the user’s vibe and their general energy level, rather than relying on only one feature. The recommendations matched my intuition best in the normal test cases, where songs like “Sunrise City” ranked highly for the pop profile and songs like “Library Rain” and “Midnight Coding” ranked highly for the chill lofi profile. 

---

## 6. Limitations and Bias 

One weakness I discovered is that my recommender is very sensitive to the mood feature, which means it can overfit to one preference when a user profile is conflicting. During the edge-case tests, especially with the “Metal Relaxed Paradox” profile, the system sometimes ranked non-metal songs above actual metal songs because mood carried too much influence and outweighed genre. The system also does not consider other useful features like lyrics, popularity, listening history, or artist similarity, so its view of taste is very limited. Some genres and moods are underrepresented in the dataset, which can make the recommender less accurate for users with rarer preferences and unintentionally favor users whose tastes match the more represented styles.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
