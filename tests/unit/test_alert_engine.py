
def test_process_alerts_success(alert_engine, mock_fetcher, mock_mailer):
    """Test successful log processing cycle."""
    # 1. Setup mocks
    mock_log = {'id': 101, 'level': 'ERROR', 'message': 'Disk full'}
    mock_fetcher.get_unprocessed_logs.return_value = [mock_log]
    mock_fetcher.try_claim_log.return_value = True
    
    # 2. Run
    alert_engine.process_alerts()
    
    # 3. Assertions
    mock_mailer.send.assert_called_once()
    mock_fetcher.mark_as_alerted.assert_called_once_with(101, status='SENT')

def test_process_alerts_claim_failed(alert_engine, mock_fetcher, mock_mailer):
    """Test that if we cannot claim a log, email is NOT sent."""
    # 1. Setup: Claim fails (e.g., another worker grabbed it)
    mock_log = {'id': 102, 'level': 'CRITICAL', 'message': 'Out of memory'}
    mock_fetcher.get_unprocessed_logs.return_value = [mock_log]
    mock_fetcher.try_claim_log.return_value = False
    
    # 2. Run
    alert_engine.process_alerts()
    
    # 3. Assertions
    mock_mailer.send.assert_not_called()
    mock_fetcher.mark_as_alerted.assert_not_called()

def test_process_alerts_mailer_exception(alert_engine, mock_fetcher, mock_mailer):
    """Test that if mailer fails, log is marked as FAILED."""
    # 1. Setup
    mock_log = {'id': 103, 'level': 'ERROR', 'message': 'DB conn error'}
    mock_fetcher.get_unprocessed_logs.return_value = [mock_log]
    mock_fetcher.try_claim_log.return_value = True
    mock_mailer.send.side_effect = Exception("SMTP connection lost")
    
    # 2. Run
    alert_engine.process_alerts()
    
    # 3. Assertions
    mock_fetcher.mark_as_alerted.assert_called_once_with(103, status='FAILED')