import os
import json
import logging
import warnings
import argparse

from flask import Flask, jsonify, request
from flask_api import status
from flask_cors import CORS
from flask_caching import Cache

from src.llm import LLMWrapper

app_name = 'LLMRepairCrawler Flask server'
llm_wrapper: LLMWrapper = None

app = Flask(app_name)
CORS(app)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)


@app.route("/dataset", methods=["GET"])
@cache.cached(query_string=True)
def retrieve_dataset():
    global llm_wrapper

    params = request.args
    dataset_id = params.get("dataset_id")
    source = params.get("source")
    logging.debug(f"[{request.method}]: dataset request with args ({json.dumps(params)}).")

    if dataset_id is None:
        return "No dataset_id provided.", status.HTTP_400_BAD_REQUEST
    if source is None:
        return "No source provided.", status.HTTP_400_BAD_REQUEST

    if llm_wrapper is None:
        llm_wrapper = LLMWrapper()

    if source == "osm":
        llm_wrapper.load_osm(dataset_id)
        return jsonify(llm_wrapper.osm_dataset)
    else:
        llm_wrapper.load_apify(dataset_id)
        return jsonify(llm_wrapper.apify_dataset)


@app.route("/answer", methods=["GET"])
@cache.cached(query_string=True)
def retrieve_answer():
    global llm_wrapper

    params = request.args
    question = params.get("question")
    dataset_id = params.get("dataset_id")
    source = params.get("source")
    logging.debug(f"[{request.method}]: answer request with args ({json.dumps(params)}).")

    if question is None:
        return "No question provided.", status.HTTP_400_BAD_REQUEST
    if dataset_id is None:
        return "No dataset_id provided.", status.HTTP_400_BAD_REQUEST
    if source is None:
        return "No source provided.", status.HTTP_400_BAD_REQUEST

    if llm_wrapper is None:
        llm_wrapper = LLMWrapper()

    if source == "osm":
        llm_wrapper.load_osm(dataset_id)
        result = llm_wrapper.answer_osm(dataset_id, question)
    else:
        llm_wrapper.load_apify(dataset_id)
        result = llm_wrapper.answer_apify(dataset_id, question)

    return jsonify(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=app_name)
    parser.add_argument('port', type=int, help='Server port')
    parser.add_argument('debug', type=bool, help='Debug mode')
    parser.add_argument('log', type=str, help='Log file')

    args = parser.parse_args()

    logging.basicConfig(filename=args.log, filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    warnings.filterwarnings("ignore")
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    logging.info(f"Running {app_name}")
    app.run(host='0.0.0.0', threaded=True, debug=args.debug, port=args.port)
