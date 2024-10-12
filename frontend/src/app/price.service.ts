import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { InputService } from './input.service';

@Injectable({
  providedIn: 'root',
})
export class PriceService {
  price: number = 0;

  constructor(private http: HttpClient, private inputService: InputService) {}

  predictPrice(inputData: { [column: string]: any[] }): void {
    this.inputService.makeRequest(inputData).subscribe({
      next: (response) => {
        this.makeRequest(response['processed_input']);
      },
      error: (error) => {
        console.error("Couldn't post input due to ", error);
      },
    });
  }

  makeRequest(processedInput: { [column: string]: any[] }): void {
    this.http
      .post<any>(
        'http://localhost/api/prediction',
        processedInput
      )
      .subscribe({
        next: (response) => {
          this.price = response['price_in_lacs'];
        },
        error: (error) => {
          console.log("Couldn't predict price due to ", error);
        },
      });
  }

  getPrice(): number {
    return this.price;
  }
}
