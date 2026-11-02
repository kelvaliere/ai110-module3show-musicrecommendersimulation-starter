# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

> Explain your design in plain language.
> 
> how Some prompts to answer:
> - What features does each `Song` use in your system
>   - For example: genre, mood, energy, tempo
> - What information does your `UserProfile` store
> - How does your `Recommender` compute a score for each song
> - How do you choose which songs to recommend

Real-world recommendations focus on behaviors from users, and filtering based on liked genres and songs. A neural network can use vectors and share it to people who may like the same songs as you do.

The system ranks candidate songs and albums on a scale using the data from your account (likes, searches, previously liked genres). It will consistently rerank to show new recommendations, thus creating a loop.

For my version, I want to make a bigger emphasis on liked songs and the amount of time spent listening to those songs. I am looking to calculate that score to figure out the users' favorite songs of alltime, and use those related genres to build a recommendation system that may have the same type of sounds.

The `Song` objects will have a focus on the genre, energy, and potentially the BPM to provide the user similar sounding album recommendations. My `UserProfile` will store top genres, energy, and favorite sounds, if possible for the user to favorite certain genres and artists.

### Algorithm Recipe
| **Weight name**             | **Weight** |
|-----------------------------|------------|
| Plays                       | 1.0 (up to x1.25 in favorite genre, growing with plays) |
| Genre match                 | 1.0        |
| Genre bonus from song plays | 0.5        |
| Energy, acoustics, mood     | 4.5        |

Some plausible biases are on how genres are affected, a user whose favorite genre is rock may not enjoy heavy metal. Users may also enjoy songs with various different moods, ex. sad pop and happy rock.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```zsh
============================================================
                    TOP RECOMMENDATIONS                     
============================================================

1. Sunrise City                                Score:  5.55
     - energy 0.82 vs target (+1.96)
     - acousticness fit (+0.98)
     - mood matches (+1.50)
     - genre matches (+1.00)
     - matches search 'neon' (x1.02)

2. Rooftop Lights                              Score:  4.67
     - played 4x
     - energy 0.76 vs target (+1.92)
     - acousticness fit (+0.85)
     - mood matches (+1.50)

3. Gym Hero                                    Score:  3.59
     - energy 0.93 vs target (+1.74)
     - acousticness fit (+0.85)
     - genre matches (+1.00)

4. Life on Mars?                               Score:  3.15
     - energy 0.50 vs target (+1.40)
     - acousticness fit (+0.75)
     - genre matches (+1.00)

5. Night Drive Loop                            Score:  2.94
     - energy 0.75 vs target (+1.90)
     - acousticness fit (+0.98)
     - matches search 'neon' (x1.02)
============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



