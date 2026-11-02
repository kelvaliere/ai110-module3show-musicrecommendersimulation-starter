# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  

**Know Your New Favorite Songs At Every Age**: A recommendation model based on your favorite genres and listening habits
> (name is based off the song *Know Who You Are At Every Age*, from the album **Four-Calendar Cafe** by Cocteau Twins)

---

## 2. Intended Use  

> Describe what your recommender is designed to do and who it is for. 
> 
> Prompts:  
> 
> - What kind of recommendations does it generate  
> - What assumptions does it make about the user  
> - Is this for real users or classroom exploration  

The recommender is designed to generate new recommendations of music based on your favorite tracks and genres. It makes assumptions based on your listening habits, such as the songs you like and the search terms in your history to further personalize your preferences and user profile.

This is meant as an experimental system, and could be integrated with Last.fm and Album Of The Year in the near future, including an optional reviews section to see if others like the album.

---

## 3. How the Model Works  

> Explain your scoring approach in simple language.  
> 
> Prompts:  
> 
> - What features of each song are used (genre, energy, mood, etc.)  
> - What user preferences are considered  
> - How does the model turn those into a score  
> - What changes did you make from the starter logic  
> 
> Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The main features noted are the genre and the amount of plays. Songs that are within the genre get an small extra weight, since the genre is an umbrella term, we cannot assume that users would enjoy subgenres.

BPMs of songs are also considered, and the result will show whether the user enjoys faster or slower tracks.

The model calculates the bonus points from the favorite genre by adding the genre's score (`+ 1.0`), followed by an incremental multiplier. The more the user engages with a certain genre, the score will scale alongside that genre to create a better ranking.

---

## 4. Data  

> Describe the dataset the model uses.  
> 
> Prompts:  
> 
> - How many songs are in the catalog  
> - What genres or moods are represented  
> - Did you add or remove data  
> - Are there parts of musical taste missing in the dataset  

I did not add new columns, but I included some songs from David Bowie, The Velvet Underground, The Beatles, and Joy Division to have a diverse mix into the dataset.

However, most of the songs added are mostly `rock`, with the exception of a song by David Bowie that is `pop`.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

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
