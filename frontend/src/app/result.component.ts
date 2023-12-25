import { Component } from '@angular/core';
import { PriceService } from './price.service';

@Component({
  selector: 'app-result',
  template: `
    <h6
      class="result top-spacing horizontal-center"
      *ngIf="priceService.getPrice() > 0"
    >
      {{ "Price in lacs: Rs. " + priceService.getPrice().toFixed(2) }}
    </h6>

  `,
  styles: [`
    .result {
      background-color: #dff0d8;
      color: #3c763d;
      border: 1px solid #d6e9c6;
      padding: 10px;
      border-radius: 5px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease-in-out;
    }

    .result:hover {
      transform: scale(1.05);
      box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }

  `],
})
export class ResultComponent {
  constructor(public priceService: PriceService) {}
}

