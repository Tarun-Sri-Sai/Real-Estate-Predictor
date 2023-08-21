import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div class="container">
      <div class="row">
        <div class="col-md-4 offset-md-4">
          <app-title></app-title>
          <app-input></app-input>
          <app-result></app-result>
        </div>
      </div>
    </div>

  `,
  styles: [`

  `],
})
export class AppComponent {}

