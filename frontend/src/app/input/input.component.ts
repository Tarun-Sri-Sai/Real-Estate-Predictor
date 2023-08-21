import { Component } from '@angular/core';
import { ColumnsService } from '../columns.service';
import { DataValuesService } from '../data-values.service';
import { InputService } from '../input.service';
import { PriceService } from '../price.service';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css'],
})
export class InputComponent {
  inputData: { [column: string]: any } = {};
  selectedOption: { [column: string]: any } = {};

  constructor(
    public columnsService: ColumnsService,
    public dataValuesService: DataValuesService,
    private priceService: PriceService
  ) {}

  transformColumnName(column: string): string {
    return column
      .split('_')
      .map((word) => {
        if (word.includes('/')) {
          return word.toUpperCase();
        }
        return word.charAt(0).toUpperCase() + word.slice(1);
      })
      .join(' ');
  }

  sendInput(): void {
    this.getInputData();
    for (let column of this.columnsService.getColumns()) {
      if (!this.inputData[column]) {
        return;
      }
    }
    this.priceService.predictPrice(this.inputData);
  }

  getInputData(): void {
    for (let column of this.columnsService.getColumns()) {
      this.inputData[column] = this.selectedOption[column];
    }
  }

  customSearch(term: string, item: any): boolean {
    return item.toString().toLowerCase().includes(term.toLowerCase());
  }

  isEncoded(column: string): boolean {
    return this.dataValuesService.getDataValues().hasOwnProperty(column);
  }
}
