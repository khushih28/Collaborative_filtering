from flask import Flask,render_template,request
import pickle
import numpy as np

pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        print(f"User input received: {user_input}")
        
        index = np.where(pt.index == user_input)[0][0]
        print(f"Book index: {index}")
        
        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:5]
        print(f"Similar items: {similar_items}")

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            if temp_df.empty:
                print(f"No data found for book index: {i[0]}")
                continue
            
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        print(f"Final recommendation data: {data}")
        return render_template('recommend.html', data=data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('recommend.html', error=str(e))



if __name__ == "__main__":
    app.run(debug=True)