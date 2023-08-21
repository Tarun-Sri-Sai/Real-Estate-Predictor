import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';

import { AppComponent } from './app.component';
import { TitleComponent } from './title/title.component';
import { ResultComponent } from './result/result.component';
import { InputComponent } from './input/input.component';

@NgModule({
  declarations: [AppComponent, TitleComponent, ResultComponent, InputComponent],
  imports: [BrowserModule, HttpClientModule, FormsModule, NgSelectModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
