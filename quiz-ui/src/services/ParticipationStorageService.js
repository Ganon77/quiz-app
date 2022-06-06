export default {
  clear() {
    localStorage.removeItem('playerName')
  },
  savePlayerName(playerName) {
    if(playerName){
      console.log(playerName)
      localStorage.setItem("playerName", playerName);
    }      
    else
      console.log("playerName undefined")
  },
  getPlayerName() {
    return localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    localStorage.setItem("score", participationScore);
  },
  getParticipationScore() {
    return localStorage.getItem("score");
  },
  saveAccessToken(token) {
    localStorage.setItem("token", token);
  },
  getAccessToken() {
    return localStorage.getItem("token");
  },
  deleteAccessToekn(){
    localStorage.removeItem('token');
  }
};