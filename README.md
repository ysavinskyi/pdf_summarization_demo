## **Description**

This project is a demonstration of custom API interface that implements prompt engineering techniques to deliver the result.

Its APIs pre-process the data and send it to the LLM model using OpenAI API, and then return its processes response.

The features represented by API:

- PDF context summarization. Accepts a PDF file as input and returns its summarized **text** content
- General LLM query. Can answer generic requests, answers or specific tasks (*hostname:5000/generic_message*)

## **Deployment / Usage**

The application is containerized by Docker (`./docker_image.tar`), so it can be deployed accordingly:

#### 1. Load the archived image to Docker (example for Unix)
```
sudo docker load -i ./docker_image.tar
```
#### 2. Validate and get the repo name and tag
```
sudo docker images
```
this way you will be able to see actual name and tag of image (*pdf_summarization_demo:latest*)
#### 3. Run the application container
```commandline
docker run -p 5000:5000 pdf_summarization_demo:latest
```

After that, you will be able to send requests to 127.0.0.1 hostname (debug server).

In case you need to run image on another host name, consider updating `app_run.py`:13 as below:
```commandline
app.run(host='0.0.0.0', port=<desired_port>)
```
and adjusting `DockerFile` accordingly.

## **Feature specifications** 
### 1. summarize_pdf

This API method is used by sending **POST** request to  *hostname:5000/summarize_pdf* of following structure:

Using Python `requests`module

```
requests.post(
              url,
              files={'file': <your_pdf_file_object>},
              data={'api_key': <your_OpenAI_token>}
)
```

or using `curl` system utility
```commandline
curl -X POST <url> \
     -F "file=@<path_to_your_pdf_file>" \
     -F "api_key=<your_OpenAI_token>"
```

where `<your_OpenAI_token>` meant to be provided as plain string.

Under the hood, method uses request to GPT-4 model to request summarization of the text extracted from PDF file.

The set of query parameteres used:
```commandline     
        model='gpt-4',
        validator_name='rouge',
        n_answers=3,   
        max_tokens=300,
        temperature=0.2,
```

The `validator_name` attribute defines the algorithm used for prompt result validation.
This way the best scored answer from range of `n_answers` will be passed as optimal response.


### 1. generic_message

The method handles simple Zero-shot or Few-shot prompts sent via **POST** request to *hostname:5000/summarize_pdf* in same ways as previous:

Using Python `requests`module

```
requests.post(
              url,
              data={'api_key': api_key, 'message': <your_request>}
)
```

or using `curl` system utility
```commandline
curl -X POST <url> \
     -d "api_key=<your_api_key>" \
     -d "message=<your_request>"
```

The input provided in `<your_request>` can differ according to the purpose you're following:

*One plain string*. This way the role of request owner will be considered always as `User`
```commandline
data={'api_key': api_key, 
      'message': 'Who is the biggest cat living?'}
```

*List of plain strings*. As in previous case, the role is set to `User` by default
```commandline
data={'api_key': api_key, 
      'message': ['Who is the biggest cat living?', 'What was the first cat name?']}
```

*Dictionary with few shots*. The roles of messages interpreted accordingly as initial. 
This approach will be helpful in creating Few-shot prompts. 
```commandline
data={'api_key': api_key, 
      'message': [
                    {'role': 'user', 'content': 'Who is the biggest cat living?'}, 
                    {'role': 'assistant', 'content': 'The biggest cat is a liger named Hercules'},
                    {'role': 'user', 'content': 'Who is he named after?'},
                 ]}
```

### Response structure
The uniform of API resonse is structured as following:
```commandline
{
        'model_response': <text_of_model_response>,
        'metrics': <validation_metrics_used>
    }
```
containing the text of best response defined and the metrics used to evaluate it.


## Support

Once any question or issue arise when using following scrip, feel free to submit email to *sservelynx@gmail.com*.