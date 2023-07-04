import { Component } from '@angular/core'
import { AppService } from '../app.service'

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent {
  constructor(public app: AppService) { }
}
