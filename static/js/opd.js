var appUrlBase = 'http://localhost:5000/'
var alertDisplayTime = 10000;   // in milliseconds

$.fn.exists = function (callback) {
    var args = [].slice.call(arguments, 1);
    if (this.length)
        callback.call(this, args);
    return this;
};

$(function () {
    $('.alert-box .alert').each(function () {
        var thisAlert = $(this);
        setTimeout(function () {
            thisAlert.slideUp();
        }, alertDisplayTime);
    });

    $('.alert-box .alert .close').click(function () {
        var alert = $(this).parent('.alert');
        alert.slideUp();
    });


    $(".clickable-row").click(function () {
        window.location = $(this).data("href");
    });


    $('.nav-tabs>li').each(function () {
        var keyword = $(this).data('active-on')
        if (window.location.href.indexOf(keyword) > -1) {
            $(this).addClass('active');
        }
    });


    $('.link-confirm').click(function (e) {
        var question = $(this).data('question') || 'คุณแน่ใจหรือไม่?';
        var answer = confirm(question);
        if (!answer) {
            e.preventDefault();
        }
    });


    // appointment making
    $('#appointment-confirm').exists(function () {
        $('#appointment-confirm').hide();
        if (docId && deptId) {
            $('select[name=dept]').val(deptId);
            setDept(deptId, function () {
                $('select[name=doctor]').val(docId);
                setDoctor(docId);
            }, docId);
        }

        //$('#appointment-calendar').hide();
        $('select[name=dept]').change(function () {
            setDept($(this).val());
        });
        $('select[name=doctor]').change(function () {
            setDoctor($(this).val());
        });

        function selectShift() {
            var cell = $(this).closest('#appointment-calendar td.available');

            clearShiftSelection();

            $('input[name=date]').val(cell.data('date'));
            $('select[name=shift]').val($(this).data('shift'));

            var availableDoctors = $(this).data('available');
            // random doctor from the list
            var chosenDoctor = availableDoctors[Math.floor(Math.random() * availableDoctors.length)]
            $('input[name=doctor_chosen').val(chosenDoctor);

            $(this).addClass('selected');
            cell.addClass('selected');
        }

        function setDept(deptId, callback = function (x) {
        }, callbackParam) {
            // reset doctor select list
            $('select[name=doctor] option[value!=""]').remove();

            if (!deptId) {
                $('#appointment-calendar').hide();
                $('#appointment-calendar-null').show();
            } else {
                $('#appointment-calendar').show();
                $('#appointment-calendar-null').hide();
                console.log($('select[name=doctor]').html());
                $.get(appUrlBase + 'api/doctor/dept/' + deptId, function (data) {
                    console.log(data);
                    for (var i = 0; i < data.length; i++) {
                        var fullName = data[i].first_name + ' ' + data[i].last_name;
                        var optionDom = $('<option>');
                        optionDom.text(fullName);
                        optionDom.attr('value', data[i].user_id);
                        console.log('appending ', fullName);
                        $('select[name=doctor]').append(optionDom);
                    }
                    $('select[name=doctor]').val('');
                    console.log('calling...')
                    callback(callbackParam);
                });
                updateCalendar(deptId, false);
            }
            clearShiftSelection();
        }

        function setDoctor(docId) {
            if (docId) {
                updateCalendar(docId, true);
            }
            clearShiftSelection();
        }

        function updateCalendar(id, isDoctor = true) {
            // TODO recalculate & reset calendar
            var url = appUrlBase + 'api/schedule/available/';
            if (isDoctor)
                url += 'doctor/' + id;
            else
                url += 'dept/' + id;
            url += '?start=' + $('td.date').first().data('date');
            url += '&end=' + $('td.date').last().data('date');
            $('td.date').addClass('booked');
            $('td.date .shift').addClass('booked');
            $.get(url, function (data) {
                console.log(data);
                $('td.date').each(function () {
                    var currentDate = $(this).data('date');
                    var availableDay = currentDate in data;
                    var availableSlots = data[currentDate];
                    $(this).removeClass('booked available');
                    if (availableDay) {
                        $(this).addClass('available');
                    } else {
                        $(this).addClass('booked');
                    }

                    $(this).find('.shift').each(function () {
                        var shift = $(this).data('shift');
                        $(this).removeClass('booked available');
                        if (currentDate in data && availableSlots[shift].length > 0) {
                            $(this).addClass('available');
                            $(this).data({'available': availableSlots[shift]});
                            $(this).attr({'data-available': availableSlots[shift]});
                        } else {
                            $(this).addClass('booked');
                        }
                    });
                });

                $('#appointment-calendar button').off();
                $('#appointment-calendar button.available').click(selectShift);
            });
        }

        function clearShiftSelection() {
            $('input[name=date]').val('');
            $('select[name=shift]').val('');

            $('#appointment-calendar td.available').removeClass('selected');
            $('#appointment-calendar td button.available').removeClass('selected');
        }

        $('#appointment-request .next').click(function () {
            var countInvalid = 0;
            $('[required]').each(function () {
                if ($(this).val().trim() == "")
                    countInvalid++
            });
            if (countInvalid > 0) {
                alert("กรุณากรอกข้อมูลให้ครบถ้วน");
                return;
            }

            $('#appointment-request').hide();
            $('#appointment-confirm').show();

            // $('#appointment-confirm-hn').text($('select[name=doctor]').val());
            $('#appointment-confirm-patient').text($('input[name=patient_name]').val());
            $('#appointment-confirm-hn').text($('input[name=patient]').val());
            $('#appointment-confirm-dept').text($('select[name=dept] option:selected').text());
            $('#appointment-confirm-doctor').text($('select[name=doctor] option:selected').text());
            var dateString = $('input[name=date]').val();
            var timeString = $('select[name=shift]>option:selected').text();
            $('#appointment-confirm-datetime').text(dateString + ' ' + timeString);
        });
        $('#appointment-confirm .prev').click(function () {
            $('#appointment-request').show();
            $('#appointment-confirm').hide();
        });

        $('#new-appointment-submit').click(function () {
            $('#new-appointment-form').submit();
        });
    });


    // creating walk-in session
    $('#session-new').exists(function () {
        $('select[name=dept]').change(function () {
            var deptId = $(this).val();
            $('select[name=doctor] option').remove();
            var today = new Date().toISOString().split('T')[0];
            var currentShift = new Date().getHours() < 12 ? 'morning' : 'afternoon';
            var url = appUrlBase + 'api/schedule/dept/' + deptId;
            url += '?start=' + today + '&end=' + today;
            $.get(appUrlBase + 'api/doctor/dept/' + deptId, function (doctorInfos) {
                $.get(url, function (availableDoctors) {
                    var doctorIds = availableDoctors[today] ? availableDoctors[today][currentShift] : [];
                    var doctorNames = [];
                    for (var i = 0; i < doctorInfos.length; i++) {
                        for (var j = 0; j < doctorInfos.length; j++) {
                            if (doctorInfos[j].user_id == doctorIds[i]) {
                                doctorNames.push({
                                    userId: doctorInfos[j].user_id,
                                    fullName: doctorInfos[j].first_name + ' ' + doctorInfos[j].last_name
                                });
                                break;
                            }
                        }
                    }

                    var emptyOptionDom = $('<option value="">');
                    if (doctorNames.length > 0) {
                        emptyOptionDom.text('โปรดเลือก');
                        $('select[name=doctor]').append(emptyOptionDom);
                        for (var i = 0; i < doctorNames.length; i++) {
                            var optionDom = $('<option>');
                            optionDom.text(doctorNames[i].fullName);
                            optionDom.attr('value', doctorNames[i].userId);
                            $('select[name=doctor]').append(optionDom);
                        }
                    } else {
                        emptyOptionDom.text('ไม่มีแพทย์เข้าตรวจช่วงนี้');
                        $('select[name=doctor]').append(emptyOptionDom);
                    }
                    $('select[name=doctor]').val('');
                });
            });
        });
    });


    // schedule marking
    var isLocked = true;
    $('#schedule-table').exists(function () {
        setScheduleLock(isLocked);
        $('#schedule-table .schedule-tick').each(function () {
            if ($(this).children('.schedule-checkbox').prop('checked')) {
                $(this).addClass('available');
            }
            if ($(this).children('.schedule-dayon').length > 0) {
                $(this).addClass('dayon');
            }
            if ($(this).children('.schedule-dayoff').length > 0) {
                $(this).addClass('dayoff');
            }
        });
        $('#schedule-table .schedule-tick').click(function () {
            if (!isLocked) {
                var checkbox = $(this).children('.schedule-checkbox');
                if (!checkbox.prop('checked')) {
                    checkbox.prop('checked', true);
                    $(this).addClass('available');
                } else {
                    checkbox.prop('checked', false);
                    $(this).removeClass('available');
                }
            }
        });
        $('#schedule-table .schedule-tick .schedule-checkbox').click(function (e) {
            if (!isLocked) {
                var checkbox = $(this);
                if (!checkbox.prop('checked')) {
                    checkbox.prop('checked', true);
                    $(this).parent().addClass('available');
                } else {
                    checkbox.prop('checked', false);
                    $(this).parent().removeClass('available');
                }
            }
        });
        $('#schedule-unlock').click(function () {
            isLocked = false;
            setScheduleLock(isLocked);
        });
        $('#schedule-save').click(function () {
            isLocked = true;
            setScheduleLock(isLocked);
            shiftValue = ""
            $('.schedule-checkbox').each(function () {
                if ($(this).prop('checked')) {
                    if (shiftValue !== "") {
                        shiftValue += ",";
                    }
                    shiftValue += $(this).val()
                }
            });
            $('#schedule-shift-data').val(shiftValue);
            $('#schedule-shift').submit();
        });

        function setScheduleLock(isLock) {
            $('#schedule-table .schedule-tick .schedule-checkbox').prop('disabled', isLock);
            if (isLock) {
                $('#schedule-save').hide();
            } else {
                $('#schedule-save').show();
            }
        }
    });

    // session prescriptions list
    $('#session-record').exists(function () {
        var row = getPrescriptionItemTemplate();
        var sessionStatus = $('#session-info').data('status');

        // pre-fill
        if (sessionStatus > 1) {
            if (fillPrescriptions.length)
                $('#sess-prescriptions-list').empty();
            for (var i = 0; i < fillPrescriptions.length; i++) {
                $('#sess-prescriptions-list').append(getPrescriptionItemTemplate(fillPrescriptions[i]));
            }
        } else {
            $('#sess-prescriptions-list').empty();
            $('#sess-prescriptions-list').append(row.clone());
            $('#sess-add-prescription').click(function () {
                $('#sess-prescriptions-list').append(row.clone());
            });
            $('#sess-prescriptions-list').delegate('.prescriptions-remove', 'click', function () {
                $(this).closest('.prescriptions-item').remove();
            });
        }

        function getPrescriptionItemTemplate(fill = null) {
            var row = $('<tr class="prescriptions-item">');
            var nameCell = $('<td>');
            var instCell = $('<td>');
            var doseCell = $('<td>');
            var deleteCell = $('<td>');
            var nameInput = $('<input class="form-control" type="text" name="prescriptions-name[]" value="">');
            var instInput = $('<input class="form-control" type="text" name="prescriptions-instructions[]" value="">');
            var doseInput = $('<input class="form-control" type="text" name="prescriptions-dose[]" value="">');
            var deleteInput = $('<button type="button" class="btn-link prescriptions-remove"><span class="glyphicon glyphicon-remove"></span></button>');
            nameCell.append(nameInput);
            instCell.append(instInput);
            doseCell.append(doseInput);
            if (!(fill && fill.readOnly)) {
                deleteCell.append(deleteInput);
            }
            row.append(nameCell);
            row.append(instCell);
            row.append(doseCell);
            row.append(deleteCell);

            if (fill) {
                nameInput.val(fill.name);
                instInput.val(fill.usage);
                doseInput.val(fill.dosage);
                if (fill.readOnly) {
                    nameInput.prop('readonly', true);
                    instInput.prop('readonly', true);
                    doseInput.prop('readonly', true);
                }
            }

            return row;
        }
    });

    $('#create-user').exists(function () {
        $('#create-user select[name=role]').change(function () {
            var role = $(this).val();
            if (role == 'doctor' || role == 'nurse')
                $('#create-user select[name=dept]').prop('disabled', false);
            else
                $('#create-user select[name=dept]').prop('disabled', true);
        });
    });
});
