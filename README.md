# 🎬 Movie Recommender System

A content-based movie recommendation system that suggests similar movies based on your selection. The system uses TMDB (The Movie Database) data and provides movie recommendations along with their posters.
Hosted on HuggingFace https://huggingface.co/spaces/0UNknowN1/MovieRecommendation-aman
## Features

- Interactive web interface built with Streamlit
- Movie recommendations based on content similarity
- Real-time movie poster fetching from TMDB API
- Top 5 movie recommendations display
- User-friendly dropdown selection of movies

## Tech Stack

- Python 3.13
- Streamlit
- Pandas
- NumPy
- Requests (for API calls)
- Pickle (for model storage)

## Project Structure

```
├── app.py                  # Main application file
├── movie_dict.pkl         # Preprocessed movie data
├── similarity.pkl         # Pre-computed similarity matrix
├── requirements.txt       # Python dependencies
└── archive/              # Raw data folder
    ├── tmdb_5000_credits.csv
    └── tmdb_5000_movies.csv
```

## Installation

1. Clone the repository or download the files

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and go to the URL shown in the terminal (typically http://localhost:8501)

3. Select a movie from the dropdown menu

4. Click the "Recommend" button to get similar movie recommendations

## How It Works

1. **Data Processing**: 
   - The system uses TMDB movie dataset with 5000 movies
   - Movie features are extracted from various attributes like genres, keywords, cast, crew, etc.
   - This processed data is stored in `movie_dict.pkl`

2. **Similarity Computation**:
   - A similarity matrix is computed based on the movie features
   - The matrix is pre-computed and stored in `similarity.pkl`
   - This enables quick retrieval of similar movies

3. **Movie Recommendation**:
   - When a movie is selected, the system finds the most similar movies using the pre-computed similarity matrix
   - Top 5 most similar movies are recommended
   - Movie posters are fetched in real-time from TMDB API

## Dependencies

Key dependencies include:
- streamlit==1.49.0
- pandas==2.3.2
- numpy==2.3.2
- requests==2.32.5

For a complete list of dependencies, see `requirements.txt`

## API Integration

The system uses TMDB API to fetch movie posters. The API endpoint used is:
```
https://api.themoviedb.org/3/movie/{movie_id}
```

## Future Improvements

- Add movie descriptions and ratings
- Implement collaborative filtering
- Add movie trailers
- Include user ratings and reviews
- Add genre-based filtering
- Implement advanced search functionality

## Contributing

Feel free to fork this repository and submit pull requests. You can also open issues for bugs or feature requests.

## License

This project is open-source and available under the MIT License.
