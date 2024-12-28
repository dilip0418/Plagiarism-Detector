import os
import unicodedata
import convert
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Plagiarism_Detector():
    def vectorize(self, text):
        """Convets the documents(text data) into tf-idf vectors"""
        vectorizor = TfidfVectorizer(ngram_range=(3, 3))
        x = vectorizor.fit_transform(text)
        return x.toarray(), vectorizor.get_feature_names_out()

    def similarity(self, file1, file2):
        """Generates the similarity Index"""
        return cosine_similarity([file1, file2])

    def check_plagiarize(self, file_contents, files):
        """Detects plagiarism with respect to the given files"""
        plagiarism_results = set()
        vectors, features = self.vectorize(file_contents)
        # print(features)
        vecs = list(zip(files, vectors))
        # print(vecs)
        for file_a, text_vec_a in vecs:
            new_vectors = vecs.copy()
            current_idx = new_vectors.index((file_a, text_vec_a))
            del new_vectors[current_idx]
            for file_b, text_vec_b in new_vectors:

                similarity_score = self.similarity(
                    text_vec_a, text_vec_b)[0][1]
                pair = sorted((file_a, file_b))
                score = (pair[0], pair[1], round(similarity_score*100, 2))
                plagiarism_results.add(score)
        return plagiarism_results

    def file_type_detctor_local(self):
        """"Detects the type of file that is input"""
        files = [doc for doc in os.listdir(r'.\sample_files') if not doc.endswith(
            '.txt') and not doc.endswith('.py')]
        # convert = gani.converter()
        file_contents = []
        for file in files:
            if file.endswith('.docx'):
                file_contents.append(convert.word_to_txt(
                    r'D:\PROJECT_TESTING\sample_files\\'+file))
            elif file.endswith('.pdf'):
                file_contents.append(convert.pdf_to_txt(
                    r'D:\PROJECT_TESTING\sample_files\\'+file))
            elif file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.bmp'):
                file_contents.append(convert.png_to_txt(
                    r'D:\PROJECT_TESTING\sample_files\\'+file))
        # print(file_contents)

        file_contents[0] = unicodedata.normalize('NFKD', file_contents[0])
        # print(file_contents)
        results = self.check_plagiarize(file_contents, files)
        for i in results:
            print(i)

    def file_type_detctor_online(self, file):
        """"Detects the type of file that is input"""
        # convert = converter()
        file_content = ''

        if file.endswith('.docx'):
            file_content += convert.word_to_txt(r'.\sample_files\\'+file)
            file_content = unicodedata.normalize('NFKD', file_content)
        elif file.endswith('.pdf'):
            file_content += convert.pdf_to_txt(r'.\sample_files\\'+file)
        elif file.endswith('.jpg') or file.endswith('.png') or file.endswith('jpeg') or file.endswith('.bmp'):
            file_content += convert.png_to_txt(r'.\sample_files\\'+file)

        return file_content