import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MapComponent } from './map/map.component'

const appRoutes: Routes = [
  {
    path: '',
    component: MapComponent
  }
];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
