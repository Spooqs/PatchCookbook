import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { SlotData } from './patch-display/patch-display.component'

import * as Patches from '../assets/patches.json'


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    title = 'Patch Cookbook';

    deviceControl = new FormControl();
    categoryControl = new FormControl();
    patchControl = new FormControl();

    device_name = "--select--";
    is_device_selected  = false;
    devices : string[] = Object.keys(Patches);

    category_name  = "--select--";
    is_category_selected  = false;
    categories : string[] = [];
    cat_objs : any;

    patch_name = "--select--";
    is_patch_selected = false;
    patches : string[] = [];
    patch_objs : any;

    patch : any;

    slot_data :  { [key : string] : SlotData } = {};

    ngOnInit() {
    }


    onDeviceChange(event : Event) {
        console.log(event);
        if (this.deviceControl.value) {
            let newValue = (event as unknown) as string;
            this.device_name = newValue;
            this.is_device_selected = true;
            this.is_category_selected = false;
            this.is_patch_selected = false;
            this.category_name = "--select--";
            this.patch_name = "--select--";
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            this.cat_objs = (Patches as any)[newValue];
            this.categories = Object.keys(this.cat_objs);
        }
    }

    onCategoryChange(event : Event) {
        console.log(event);
        if (this.deviceControl.value && this.categoryControl.value) {
            let newValue = (event as unknown) as string;
            this.category_name = newValue;
            this.is_category_selected = true;
            this.is_patch_selected = false;
            this.patch_name = "--select--";
            this.patch_objs = this.cat_objs[newValue];
            this.patches = Object.keys(this.patch_objs);
        }
    }

    onPatchChange(event : Event) {
        console.log(event)
        if (this.deviceControl.value && this.categoryControl.value && this.patchControl.value) {
            let newValue = (event as unknown) as string;
            this.is_patch_selected = true;
            this.patch_name = newValue;
            this.patch = this.patch_objs[newValue];
            console.log(this.patch);
            this.slot_data = this.patch['recipe'];
            
        }
    }

}
