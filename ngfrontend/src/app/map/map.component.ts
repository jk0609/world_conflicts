import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AngularFireDatabase, FirebaseListObservable } from 'angularfire2/database';
import { Article } from '../article.model'
declare var google: any;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {

  articles_db: FirebaseListObservable<any[]>;
  articles: any[]

  constructor(private http: HttpClient, private database: AngularFireDatabase) {
    this.articles_db = database.list('articles');
  }




  ngOnInit() {
    // function to prevent scolling out of map bounds
    function checkBounds(map) {
      var latNorth = map.getBounds().getNorthEast().lat();
      var latSouth = map.getBounds().getSouthWest().lat();
      var newLat;
      if(latNorth<85 && latSouth>-85)
          return;
      else {
          if(latNorth>85 && latSouth<-85)
              return;
          else {
              if(latNorth>85)
                  newLat =  map.getCenter().lat() - (latNorth-85);
              if(latSouth<-85)
                  newLat =  map.getCenter().lat() - (latSouth+85);
          }
      }
      if(newLat) {
        var newCenter= new google.maps.LatLng( newLat ,map.getCenter().lng() );
        map.setCenter(newCenter);
      }
    }

    // subscribe to Firebase and generate map, markers and info window click function
    this.articles_db.subscribe(dataLastEmittedFromObserver => {
      this.articles = dataLastEmittedFromObserver;

      var mapProp = {
          center: new google.maps.LatLng(51.508742, -0.120850),
          zoom: 3,
          minZoom: 3,
          mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

      // runs checkBound if user is trying to scoll out of bounds
      google.maps.event.addListener(map, 'center_changed', function() {
          checkBounds(map);
      });

      // defines info window
      var infowindow = new google.maps.InfoWindow({
        content: ''
      });

      // generates markers
      this.articles.forEach(function(article){
        var latlng = new google.maps.LatLng(article.lat, article.lon)

        var marker = new google.maps.Marker({
          position: latlng,
          map: map,
          title: article.title
        });
        marker.addListener('click', function() {
          infowindow.setContent(
            '<a href="'+article.url+'">'+article.title+'</a>'+
            '<br><p>'+article.summary+'</p>'
          );
          infowindow.open(map, marker);
        });

      })
      // console.log(this.articles)
    })

  }

  newArticles(){
    console.log('API call')
    this.http.get('http://localhost:5000/worldconflict/api/v1.0/articles').subscribe(data => {
      var articles = this.articles_db
      var dataArticles = data['articles'];
      dataArticles.forEach(function(article){
        var newArticle = new Article(
          article.title,
          article.summary,
          article.url,
          article.lat,
          article.lon,
          article.name,
          article.country
        )
        articles.push(newArticle)
      })
    });
  }

  getArticles(){
    return this.articles;
  }

}
