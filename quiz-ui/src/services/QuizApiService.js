import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };

    console.log(`${import.meta.env.VITE_API_URL}/${resource}`)

    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getAllQuestions() {
    return this.call("get", "questions");
  },
  getQuestion(position) {
    return this.call("get", "questions/" + position);
  },
  registerParticipation(payload) {
    return this.call("post", "participations", payload);
  },
  login(payload){
    return this.call("post", "login", payload);
  },
  changeQuestion(method, body, token, oldPosition){
    return this.call(method, "questions/"+oldPosition, body, token);
  },
  addQuestion(body, token){
    return this.call("post", "questions", body, token);
  },
  deleteQuestion(token, position){
    return this.call("delete", "questions/"+position, null, token);
  }
};