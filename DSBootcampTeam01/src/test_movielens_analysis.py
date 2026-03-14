import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import pytest
import datetime
from unittest.mock import patch
from movielens_analysis import Ratings, Tags, Movies, Links
from collections import OrderedDict

@pytest.fixture
def sample_tags():
    return [
        {"userId": 1, "movieId": 4878, "tag": "time travel", "timestamp": 1234567890},
        {"userId": 2, "movieId": 4878, "tag": "sci-fi", "timestamp": 1234567891}
    ]

@pytest.fixture
def sample_movies():
    return [
        {"movieId": 1, "title": "Toy Story (1995)", "genres": "Adventure|Animation|Children|Comedy|Fantasy"},
        {"movieId": 2, "title": "Jumanji (1995)", "genres": "Adventure|Children|Fantasy"}
    ]

@pytest.fixture
def sample_links():
    return [
        {"movieId": 1, "imdbId": 114709, "tmdbId": 862},
        {"movieId": 2, "imdbId": 113497, "tmdbId": 8844}
    ]

# Fixtures for test objects
@pytest.fixture
def ratings():
    r = Ratings("src/ml-latest-small/ratings.csv", limit=1000)
    # Always override with mock data for tests
    r.data = [
        {"userId": 1, "movieId": 1, "rating": 4.5, "timestamp": 1234567890},
        {"userId": 1, "movieId": 2, "rating": 3.0, "timestamp": 1234567891},
        {"userId": 2, "movieId": 1, "rating": 5.0, "timestamp": 1234567892},
        {"userId": 2, "movieId": 2, "rating": 2.5, "timestamp": 1234567893}
    ]
    return r

@pytest.fixture
def tags():
    t = Tags("src/ml-latest-small/tags.csv", limit=1000)
    # Use sample/mock data for tests
    t.data = [
        {"userId": 1, "movieId": 1, "tag": "funny", "timestamp": 1234567890},
        {"userId": 2, "movieId": 2, "tag": "action", "timestamp": 1234567891}
    ]
    return t

@pytest.fixture
def movies():
    return Movies("src/ml-latest-small/movies.csv", limit=1000)

@pytest.fixture
def links():
    return Links("src/ml-latest-small/links.csv", limit=1000)

class TestRatings:
    def test_get_all(self,ratings):
        data=ratings.get_all()
        assert isinstance(data, list)
        assert all(isinstance(row, dict) for row in data)
        assert all(isinstance(row["rating"], float) for row in data)

    def test_get_by_userId(self, ratings):
        user_ratings = ratings.get_by_userId(1)
        assert isinstance(user_ratings, list)
        if user_ratings:
            assert all(r["userId"] == 1 for r in user_ratings)

    def test_sorted(self,ratings):
        sorted_data=ratings.get_sorted_by_ratings(default="rating", reverse=True)
        ratings_only=[r["rating"] for r in sorted_data]
        assert ratings_only == sorted(ratings_only, reverse=True)

    def test_timestamps(self,ratings):
        timestamps=ratings.convert_timestamp_datetime()
        assert all(isinstance(t, datetime.datetime) for t in timestamps)

    def test_find_top_films(self, ratings):
        top_films = ratings.find_top_films(3)
        assert isinstance(top_films, dict)

    def test_dist_by_year(self, ratings):
        year_counts = ratings.dist_by_year()
        assert isinstance(year_counts, dict)

    def test_find_top_films_average(self, ratings):
        result = ratings.find_top_films(2, metric="average")
        assert isinstance(result, dict)

    def test_find_top_films_median(self, ratings):
        result = ratings.find_top_films(3, metric="median")
        assert isinstance(result, dict)

    def test_find_top_films_invalid_metric(self, ratings):
        with pytest.raises(ValueError):
            ratings.find_top_films(2, metric="wrong")

    def test_top_controversial(self, ratings):
        result = ratings.top_controversial(3)
        assert isinstance(result, dict)

    # Remove duplicate test_dist_by_year

    def test_top_by_num_of_ratings(self, ratings):
        result = ratings.top_by_num_of_ratings(3)
        assert isinstance(result, dict)

class TestTags:
    def test_get_all(self, tags):
        data=tags.get_all()
        assert isinstance(data, list)
        assert all(isinstance(row, dict) for row in data)
        assert all(isinstance(row["tag"], str) for row in data)

    def test_by_movieId(self, tags):
        if tags.data:
            movie_id = tags.data[0]["movieId"]
            tag_line = tags.find_tags_by_movieId(movie_id)
            assert isinstance(tag_line, str)
            assert tag_line != ""
        else:
            pytest.skip("No data to test")

    def test_most_words(self, tags):
        most_words=tags.most_words(3)
        assert isinstance(most_words, dict)
        assert all(isinstance(tag, str) for tag in most_words.keys())
        assert all(isinstance(count, int) for count in most_words.values())

    def test_find_tags_by_movieId(self, tags, sample_tags):
        tags.data = sample_tags
        tag_line = tags.find_tags_by_movieId(4878)
        assert "time travel" in tag_line

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_longest(self, n, tags):
        longest=tags.longest(n)
        assert isinstance(longest, dict)
        assert all(isinstance(tag, str) for tag in longest.keys())
        assert all(isinstance(length, int) for length in longest.values())
        assert len(longest) <= n

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_most_words_and_longest(self, n, tags, sample_tags):
        tags.data = sample_tags
        big_tags = tags.most_words_and_longest(n)
        assert isinstance(big_tags, list)
        assert all(isinstance(tag, str) for tag in big_tags)
        assert len(big_tags) <= n

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_most_popular(self, n, tags, sample_tags):
        tags.data = sample_tags
        popular_tags = tags.most_popular(n)
        assert isinstance(popular_tags, dict)
        assert all(isinstance(tag, str) for tag in popular_tags.keys())
        assert all(isinstance(count, int) for count in popular_tags.values())
        assert len(popular_tags) <= n

class TestMovies:
    def test_get_all(self, movies):
        data=movies.get_all()
        assert isinstance(data, list)
        assert all(isinstance(row, dict) for row in data)
        assert all(isinstance(row["title"], str) for row in data)

    def test_get_by_genre(self, movies):
        genre="Comedy"
        comedy_movies=movies.get_by_genre(genre)
        assert all(genre in movie["genres"] for movie in comedy_movies)

    @patch('requests.get')
    def test_search_for_film(self, mock_get, movies):
        mock_html = '''
        <html>
            <body>
                <p>This is a test paragraph.</p>
                <p>Another paragraph for testing.</p>
            </body>
        </html>
        '''
        import requests
        mock_response = requests.models.Response()
        mock_response.status_code = 200
        mock_response._content = str.encode(mock_html)
        mock_get.return_value = mock_response

        film_name = "Toy Story"
        paragraphs = movies.search_for_film(film_name)
        if paragraphs is not None:
            assert isinstance(paragraphs, list)
            assert any("test paragraph" in p.lower() for p in paragraphs)
        else:
            pytest.skip("Film not found or IMDb page inaccessible")

    def test_dist_by_genres(self, movies, sample_movies):
        movies.data = sample_movies
        genre_dist = movies.dist_by_genres()
        assert isinstance(genre_dist, dict) or isinstance(genre_dist, OrderedDict)
        assert all(isinstance(genre, str) for genre in genre_dist.keys())
        assert all(isinstance(count, int) for count in genre_dist.values())
        assert genre_dist["Adventure"] == 2
        assert genre_dist["Comedy"] == 1

    @pytest.mark.parametrize("movieId,expected_title",[
        (1, "Toy Story (1995)"),
        (2, "Jumanji (1995)"),
        (276, "Milk Money (1994)")
    ])
    def test_find_movie_with_movieId(self, movieId, expected_title, movies):
        title = movies.find_movie_with_movieId(movieId)
        assert title == expected_title

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_most_genres(self, n, movies, sample_movies):
        movies.data=sample_movies
        most_genres=movies.most_genres(n)
        assert isinstance(most_genres, dict)
        assert all(isinstance(title, str) for title in most_genres.keys())
        assert all(isinstance(count, int) for count in most_genres.values())
        assert len(most_genres) <= n
        assert list(most_genres.values())[0] >= list(most_genres.values())[-1]
        assert most_genres["Toy Story (1995)"] == 5
        assert most_genres["Jumanji (1995)"] == 3

    def test_dist_by_release(self, movies, sample_movies):
        movies.data = sample_movies
        release_dist = movies.dist_by_release()
        assert isinstance(release_dist, dict) or isinstance(release_dist, OrderedDict)
        assert all(isinstance(year, int) for year in release_dist.keys())
        assert all(isinstance(count, int) for count in release_dist.values())
        assert release_dist[1995] == 2
        assert list(release_dist.keys()) == [1995]

class TestLinks:
    def test_get_all(self, links):
        data=links.get_all()
        assert isinstance(data, list)
        assert all(isinstance(row, dict) for row in data)
        assert all(isinstance(row["imdbId"], int) for row in data)
        assert all(isinstance(row["tmdbId"], int) for row in data)
        assert all(isinstance(row["movieId"], int) for row in data)

    @patch('requests.get', autospec=True)
    def test_get_imdb(self, mock_get, links, sample_links):
        # Simulate a successful response
        class MockResponse:
            status_code = 200
            content = b"<html></html>"
        mock_get.return_value = MockResponse()
        list_of_fields = ["Runtime", "Director", "Gross"]
        list_of_movies = sample_links
        links.data = sample_links
        imdb_info = links.get_imdb(list_of_movies, list_of_fields)
        assert isinstance(imdb_info, list)
        assert len(imdb_info) == len(list_of_movies)
        for movie in imdb_info:
            assert isinstance(movie, dict)

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_top_directors(self, n, links, sample_links):
        n=850
        links.data=sample_links
        imdb_movies=links.get_imdb(sample_links, ["Director"])
        top_directors=links.top_directors(imdb_movies, n)
        assert isinstance(top_directors, dict)
        assert all(isinstance(director, str) for director in top_directors.keys())
        assert all(isinstance(count, int) for count in top_directors.values())
        assert len(top_directors) <= n

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_most_profitable(self, n, links, sample_links):
        n=700
        links.data=sample_links
        imdb_movies=links.get_imdb(sample_links, ["Budget", "Gross", "title"])
        most_profitable=links.most_profitable(imdb_movies, n)
        assert isinstance(most_profitable, dict)
        assert all(isinstance(title, str) for title in most_profitable.keys())
        assert all(isinstance(profit, int) for profit in most_profitable.values())
        assert len(most_profitable) <= n
        assert list(most_profitable.values()) == sorted(most_profitable.values(), reverse=True)
        assert all(profit >= 0 for profit in most_profitable.values())

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_most_expensive(self, n, links, sample_links):
        n=1000
        links.data=sample_links
        imdb_movies=links.get_imdb(sample_links, ["Budget", "title"])
        most_expensive=links.most_expensive(imdb_movies, n)
        assert isinstance(most_expensive, dict)
        assert all(isinstance(title, str) for title in most_expensive.keys())
        assert all(isinstance(cost, int) for cost in most_expensive.values())
        assert len(most_expensive) <= n
        assert list(most_expensive.values()) == sorted(most_expensive.values(), reverse=True)
        assert all(cost >= 0 for cost in most_expensive.values())

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_top_cost_per_minute(self, n, links, sample_links):
        n=1000
        links.data=sample_links
        imdb_movies=links.get_imdb(sample_links, ["Budget", "Runtime", "title"])
        top_costs=links.top_cost_per_minute(imdb_movies, n)
        assert isinstance(top_costs, dict)
        assert all(isinstance(title, str) for title in top_costs.keys())
        assert all(isinstance(cost, float) for cost in top_costs.values())
        assert len(top_costs) <= n
        assert list(top_costs.values()) == sorted(top_costs.values(), reverse=True)
        assert all(cost >= 0 for cost in top_costs.values())

    @pytest.mark.parametrize("n", [500, 700, 750, 800, 100])
    def test_longest(self,n, links, sample_links):
        n=1000
        links.data=sample_links
        imdb_movies=links.get_imdb(sample_links, ["Runtime", "title"])
        longest=links.longest(imdb_movies, n)
        assert isinstance(longest, dict)
        assert all(isinstance(title, str) for title in longest.keys())
        assert all(isinstance(runtime, int) for runtime in longest.values())
        assert len(longest) <= n
        assert list(longest.values()) == sorted(longest.values(), reverse=True)
        assert all(runtime > 0 for runtime in longest.values())
