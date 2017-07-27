import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AngularFireDatabase, FirebaseListObservable } from 'angularfire2/database';
import { Article } from '../article.model'

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
    this.articles_db.subscribe(dataLastEmittedFromObserver => {
      this.articles = dataLastEmittedFromObserver;
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
