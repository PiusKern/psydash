var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.Checkbox = function (props) {
    const [checked, setChecked] = React.useState(props.value);

    React.useEffect(() => {
        setChecked(props.value);
    }, [props.value]);

    function checkedHandler() {
        const newValue = !checked;
        setChecked(newValue);
        props.setValue(newValue);
    }

    return React.createElement(
        'div',
        { 
            onClick: (e) => {
                e.stopPropagation();
                checkedHandler();
            },
            style: { cursor: 'pointer', width: '100%', height: '100%', display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }
        },
        React.createElement('input', {
            type: 'checkbox',
            checked: checked,
            onChange: checkedHandler,
            style: { cursor: 'pointer' }
        })
    );
};