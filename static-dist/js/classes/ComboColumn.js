Ext.ns("Ext.my.renderer","Ext.my.grid");
Ext.define('Ext.my.grid.column.Combo', {
	extend: 'Ext.grid.column.Column',
	alias: ['widget.combocolumn'],
	alternateClassName: 'Ext.my.ComboColumn',

	gridId: undefined,

	constructor: function(cfg){
		this.callParent(arguments);

		/* Detect if there is an editor and if it at least extends a combobox, otherwise just treat it as a normal column and render the value itself */
		alert(this.editor);
		this.renderer = Ext.my.renderer.ComboBoxRenderer(this.editor, this.gridId);
	}
});
 
/* a renderer that makes a editorgrid panel render the correct value */
Ext.my.renderer.ComboBoxRenderer = function(combo, gridId) {
	/* Get the displayfield from the store or return the value itself if the record cannot be found */
	getValue = function(value) {
		var idx = combo.store.find(combo.valueField, value);
		var rec = combo.store.getAt(idx);
		if (rec) {
			return rec.get(combo.displayField);
		}
		return value;
	}
	return function(value) {
		/* If we are trying to load the displayField from a store that is not loaded, add a single listener to the combo store's load event to refresh the grid view */
		if (combo && combo.store.getCount() == 0 && gridId) {
			combo.store.on(
				'load',
				function() {
					var grid = Ext.getCmp(gridId);
					if (grid) {
						grid.getView().refresh();
					}
				},
				{
					single: true
				}
			);
			return value;
		}

		return getValue(value);
	};

};
