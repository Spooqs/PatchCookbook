import { Component, Input, SimpleChanges } from '@angular/core';

export interface SlotData {
    slot_name : string,
    text : string
}



const slot_list =  [ 'slot1', 'slot5', 'slot2', 'slot6', 'slot3', 'slot7', 'slot4', 'slot8' ];

@Component({
  selector: 'patch-display',
  templateUrl: './patch-display.component.html',
  styleUrls: ['./patch-display.component.css']
})
export class PatchDisplayComponent {
    slots = [ 'slot1', 'slot5', 'slot2', 'slot6', 'slot3', 'slot7', 'slot4', 'slot8' ];

    @Input() slot_data : { [key : string] : SlotData } = {};

    @Input() patch_name : string = '';

    @Input() patch_description : string = '';

    render_boxes : boolean = false;

    ngOnChanges(changes : SimpleChanges) {
        if ('slot_data' in changes) {
            if ((Object.keys(this.slot_data)).length > 0) {
                this.render_boxes = true;
            } else {
                this.render_boxes = false;
            }
        }
    }


}
