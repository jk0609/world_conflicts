import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { masterFirebaseConfig } from './keys';
import { AngularFireModule } from 'angularfire2';
import { AngularFireDatabaseModule } from 'angularfire2/database';

import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';
import { routing } from './app.routing';
import { AgmCoreModule } from '@agm/core';


export const firebaseConfig = {
  apiKey: masterFirebaseConfig.apiKey,
  authDomain: masterFirebaseConfig.authDomain,
  databaseURL: masterFirebaseConfig.databaseURL,
  storageBucket: masterFirebaseConfig.storageBucket
};

@NgModule({
  declarations: [
    AppComponent,
    MapComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AngularFireModule.initializeApp(firebaseConfig),
    AngularFireDatabaseModule,
    routing,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyBn0I3ixv29y4hHj0R13hxzt_eN1g9qyNs'
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
