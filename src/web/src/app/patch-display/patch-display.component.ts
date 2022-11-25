import { Component } from '@angular/core';

@Component({
  selector: 'patch-display',
  templateUrl: './patch-display.component.html',
  styleUrls: ['./patch-display.component.css']
})
export class PatchDisplayComponent {
    slots = [ 'osc_d', 'main', 'osc_c', 'lfo', 'osc_b', 'pitch', 'osc_a', 'filter' ];

}
