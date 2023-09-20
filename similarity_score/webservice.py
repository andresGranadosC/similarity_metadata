from similarity_score.similarity_score import Similarity
import sys
import json
from fastapi import FastAPI
import argparse
import uvicorn
from pydantic import BaseModel

app = FastAPI()


class Data(BaseModel):
    ground_truth: list
    generic_crawler: list

class Gen_recall_result(BaseModel):
    # Generalized recall
    score: str

class Soft_scores_result(BaseModel):
    # Soft precision recall fscore
    precision: str
    recall: str
    fscore: str


@app.get("/_ping")
async def _ping():
    pass

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.post("/gen_recall")
async def gen_recall(data: Data) -> Gen_recall_result:
    #print("ground_truth:", data.ground_truth)
    #print("generic_crawler:", data.generic_crawler)
    cs = Similarity( data.ground_truth, data.generic_crawler )
    similarity, g_recall = cs.gen_recall()
    return Gen_recall_result(score=str(g_recall))
    #return Gen_recall_result(score="1.00")


@app.post("/soft_scores")
async def soft_scores(data: Data) -> Soft_scores_result:
    #print("ground_truth:", data.ground_truth)
    #print("generic_crawler:", data.generic_crawler)
    cs = Similarity( data.ground_truth, data.generic_crawler )
    s_precision = cs.soft_precision()
    s_recall = cs.soft_recall()
    s_f_score = cs.soft_fscore()
    return Soft_scores_result(precision=str(s_precision), recall=str(s_recall), fscore=str(s_f_score) )


# def main( ground_truth, generic_crawler ):
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", action="store", default=8080, help="Port to listen on", type=int
    )
    parser.add_argument(
        "--host", action="store", default="0.0.0.0", help="Hosts to listen on", type=str
    )
    args = parser.parse_args()

    # create and run the web service
    uvicorn.run(app, host=args.host, port=args.port, reload=False)

    #print("ground_truth:", ground_truth)
    #print("generic_crawler:", generic_crawler)


#   python main.py '["Mathematik"]' '["Mathematik", "Physik", "Geometrie" ]'


if __name__ == "__main__":
    # gt = json.loads( sys.argv[1] )
    # gc = json.loads( sys.argv[2] )
    # main( gt, gc )
    main()

