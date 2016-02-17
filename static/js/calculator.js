var demo = new Vue({
    el: '#app',

    data: {
      userid: '',
      steam_id_url: '',
      owned_game_url: '',
      apikey: 'FC65FE32E5732FC54BC70256CDA122BB',
      steam_id: ''
    },

    /*
    methods: {
      reverseMessage: function() {
        this.owned_game_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + this.apikey + '&steamid=' + this.userid + '&format=json';
        this.steam_id_url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=' + this.apikey + '&vanityurl=' + this.userid;

        $.getJSON(this.steam_id_url, function(result) {
        	var jsonString = JSON.stringify(result);
        	var result = JSON.parse(jsonString);
        	console.log(result); 
          //this.steam_id = result.response.steamid;
        });
      }
    }
    */
  }

)

