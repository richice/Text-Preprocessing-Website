# Chinese Text Preprocessing API

This is a Flask based API for preprocessing Chinese text to make it better structured for downstream NLP tasks. It takes in a text input and outputs a cleaned version by performing the following:

- Split text into sentences based on punctuation  
- Remove irrelevant content like numbers, brackets, article titles
- Standardize punctuation like colons, semicolons, periods
- Join short phrases into single sentences

## Usage

- POST input text to `/preprocess_text` endpoint  
- API returns preprocessed text in response

## Example

```
Input:

第一条 为保证双方权利,订立本合同。

Output:  

为保证双方权利,订立本合同。
```

The API can be used as a preprocessing step for tasks like summarization, translation, sentiment analysis etc. To customize, modify the regex patterns in `preprocess_text()` route.

This provides simple Chinese text cleaning to generate more readable content for downstream consumption.

![image](https://github.com/richice/Text-Preprocessing-Website/assets/99071400/714c9d3b-3cf1-47cf-a124-dc6ddbe11c38)
