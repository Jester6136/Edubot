# Edubot - Admission consultant chatbot for AIA University

## :surfer: Introduction
 Edubot is a demo assistant which helps parents and students know more about majors in HCMUT and improve the possibility of students applying to the school

## 👷‍ Installation
To install Edubot, please clone the repo and run:
```sh
pip install -r requirements.txt
```
This will install the bot and all of its requirements.
Note that this bot should be used with python 3.6 or 3.7
## 🚀 Improve Edubot in Vietnamese
### 1. Vietnamese tokenize
I've used underthesea to tokenize words
### 2. Embedding
I've used pretrained word vector of fasttext
So you need to download pretrained word vector from fasttext
```bash
mkdir vi_feature
```   
```bash
wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.vi.300.bin.gz -P vi_feature
```   
## 🤖 To run Sara:

Use `rasa train` to train a model (this will take a significant amount of memory to train,
if you want to train it faster, try the training command with
`--augmentation 0`).

Then, to run, first set up your action server in one terminal window:
```bash
rasa run actions
```
Second:
```bash
rasa shell
```
## 👩‍💻 Overview of the files
`custom_nlu` - contains custom part in pipeline

`data/stories/` - contains stories 

`data/nlu` - contains NLU training data

`data/rules` - contains rules

`actions` - contains custom action code

`domain.yml` - the domain file, including bot response templates

`config.yml` - training configurations for the NLU pipeline and policy ensemble

## References: 
 - Nguyen Thi Mai Trang and Maxim Shcherbakov "Enhancing Rasa NLU model for Vietnamese chatbot" in International Journal of Open Information Technologies ISSN, 2021
 - https://github.com/RasaHQ/rasa
