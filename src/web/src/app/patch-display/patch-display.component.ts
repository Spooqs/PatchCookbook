import { Component, Input, SimpleChanges } from '@angular/core';

export interface SlotData {
    slot_name : string,
    text : string
}



const default_slot_data :  { [key : string] : SlotData } = {
    'slot1' : {
        'slot_name' : '',
        'text' : "",
    },
    'slot2' : {
        'slot_name' : "osc_c",
        'text' : "default text",
    },

    'slot3' : {
        'slot_name' : "osc_b",
        'text' : "default text",
    },

    'slot4' : {
        'slot_name' : "osc_a",
        'text' : "default text",
    },

    'slot5' : {
        'slot_name' : "main",
        'text' : "default text",
    },

    'slot6' : {
        'slot_name' : "lfo",
        'text' : "default text",
    },

    'slot7' : {
        'slot_name' : "pitch",
        'text' : "default text",
    },

    'slot8' : {
        'slot_name' : "filter",
        'text' : "default text",
    },
};

const slot_list =  [ 'slot1', 'slot5', 'slot2', 'slot6', 'slot3', 'slot7', 'slot4', 'slot8' ];

@Component({
  selector: 'patch-display',
  templateUrl: './patch-display.component.html',
  styleUrls: ['./patch-display.component.css']
})
export class PatchDisplayComponent {
    slots = [ 'slot1', 'slot5', 'slot2', 'slot6', 'slot3', 'slot7', 'slot4', 'slot8' ];

    @Input() slot_data : { [key : string] : SlotData } = {};
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
