import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PatchDisplayComponent } from './patch-display.component';

describe('PatchDisplayComponent', () => {
  let component: PatchDisplayComponent;
  let fixture: ComponentFixture<PatchDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PatchDisplayComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PatchDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
