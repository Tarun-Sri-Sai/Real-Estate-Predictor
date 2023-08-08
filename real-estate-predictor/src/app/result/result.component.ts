import { Component } from '@angular/core';
import { PriceService } from '../price.service';

@Component({
    selector: 'app-result',
    templateUrl: './result.component.html',
    styleUrls: ['./result.component.css'],
})
export class ResultComponent {
    constructor(public priceService: PriceService) {}
}
