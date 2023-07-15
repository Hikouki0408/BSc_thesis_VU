# Bachelor Thesis Computer Science 

# "Extract text from HTML pages for advanced relation extraction"
# Abstract
# HTML Parsing
Code for HTML Tag experiment is in the folder [Tag_experiment](./Tag_experiment). 
# Preprocessing
# Open IE
The relation extraction model utilized in this study is based on a Python NLP library
provided by the [StanfordCoreNLP](http://www.example.com) frame work. To extract relations or information from text, we can utilize the ’openie’ annotator within the framework. 

# Datasets
The datasets and related text are available in the folder [Datasets](./Datasets). 
# Experiment
 - Base model vs Our model
 - Run the code: 'OIE_whole.py' for base modek
 - Run the code: 'OIE_extraced_text.py' for our model
# Conclusion
Our HTML parsing approach primarily focuses on decoding HTML text contents and optimizing HTML tag identification to remove unnecessary or redundant information while preserving the relevant content securely. The preprocessing stage involves stripping the extracted text and prioritizing textual information by categorizing it into four labels. After centering the target text contents, Open IE is performed the Python NLP library provided by StanfordCoreNLP. In order to evaluate our proposed model, we conducted an experiment considering runtime, efficiency, and accuracy as evaluation aspects to assess its performance. As a result, our model successfully reduced the size of extracted text contents from Wikipedia and eBook pages while minimizing the runtime. Additionally, our model achieved higher precision, recall, and F1 score compared to the base model with both datasets, demonstrating improved accuracy. Therefore, we can conclude that our proposed model not only increases efficiency but also improve the accuracy of relation extraction, thereby ensuring the extraction of more reliable information that aligns efficiently with the primary goal of relation extraction.
