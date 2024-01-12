import requests
import logging
import time
import concurrent.futures
from tqdm import tqdm

from spectral_datawrappers.data_wrappers_interface import DataWrapperInterface
from spectral_datawrappers.config import settings


class CreditScoringWrapper(DataWrapperInterface):

    @staticmethod
    def _exported_features(): return [
        "borrow_block_number",
        "borrow_timestamp",
        "wallet_address",
        "first_tx_timestamp",
        "last_tx_timestamp",
        "wallet_age",
        "incoming_tx_count",
        "outgoing_tx_count",
        "net_incoming_tx_count",
        "total_gas_paid_eth",
        "avg_gas_paid_per_tx_eth",
        "risky_tx_count",
        "risky_unique_contract_count",
        "risky_first_tx_timestamp",
        "risky_last_tx_timestamp",
        "risky_first_last_tx_timestamp_diff",
        "risky_sum_outgoing_amount_eth",
        "outgoing_tx_sum_eth",
        "incoming_tx_sum_eth",
        "outgoing_tx_avg_eth",
        "incoming_tx_avg_eth",
        "max_eth_ever",
        "min_eth_ever",
        "total_balance_eth",
        "risk_factor",
        "total_collateral_eth",
        "total_available_borrows_eth",
        "avg_weighted_risk_factor",
        "risk_factor_above_threshold_daily_count",
        "avg_risk_factor",
        "max_risk_factor",
        "borrow_amount_sum_eth",
        "borrow_amount_avg_eth",
        "borrow_count",
        "repay_amount_sum_eth",
        "repay_amount_avg_eth",
        "repay_count",
        "borrow_repay_diff_eth",
        "deposit_count",
        "deposit_amount_sum_eth",
        "time_since_first_deposit",
        "withdraw_amount_sum_eth",
        "withdraw_deposit_diff_If_positive_eth",
        "liquidation_count",
        "time_since_last_liquidated",
        "liquidation_amount_sum_eth",
        "market_adx",
        "market_adxr",
        "market_apo",
        "market_aroonosc",
        "market_aroonup",
        "market_atr",
        "market_cci",
        "market_cmo",
        "market_correl",
        "market_dx",
        "market_fastd",
        "market_fastk",
        "market_ht_trendmode",
        "market_linearreg_slope",
        "market_macd_macdext",
        "market_macd_macdfix",
        "market_macd",
        "market_macdsignal_macdext",
        "market_macdsignal_macdfix",
        "market_macdsignal",
        "market_max_drawdown_365d",
        "market_natr",
        "market_plus_di",
        "market_plus_dm",
        "market_ppo",
        "market_rocp",
        "market_rocr",
        "unique_borrow_protocol_count",
        "unique_lending_protocol_count",
        "target",
    ]

    @staticmethod
    def _config_keys(): return ["single_wallet_url", "batch_url", "api_key"]

    def __init__(self, config: dict) -> None:
        self.config = config
        self.single_wallet_url = config["url"] if "url" in config else settings.CREDIT_SCORING_URL
        self.batch_url = config["batch_url"] if "batch_url" in config else settings.CREDIT_SCORING_BATCH_URL
        self.api_key = config["spectral_api_key"] if "spectral_api_key" in config else settings.SPECTRAL_API_KEY
        self.num_items_per_batch_request = config["num_items_per_batch_request"] if "num_items_per_batch_request" in config else settings.NUM_ITEMS_PER_BATCH_REQUEST

    @staticmethod
    def __validate_request_payload(input: dict):
        """ Checks if the minimum required fields are present in the input.

        Args:
            input (dict): Request payload.

        Raises:
            ValueError: If the input is invalid.
        """
        if 'wallet_address' not in input and 'wallets_addresses' not in input:
            raise ValueError("Missing wallet_address in input")
        if input.get('wallet_address') is None and input.get('wallets_addresses') is None:
            raise ValueError("wallet_address cannot be None")

    def request(self, input: dict) -> dict:
        """Fetches wallet credit-scoring data from Spectral's API.

        Args:
            input (dict): Request payload.

        Returns:
            dict: The response from the Credit-Scoring API.
        """
        # use self.config to fetch the data from the Data Source
        max_retries = settings.NUM_RETRIES
        retries = 0
        while retries < max_retries:
            try:
                logging.debug(
                    "Requesting Credit Scoring API with input: {}".format(input))
                self.__validate_request_payload(input)

                request_url = self.single_wallet_url.format(input["wallet_address"])
                response = requests.get(
                    url=request_url,
                    headers={"Authorization": f"bearer {self.api_key}", "Content-Type": "application/json"}
                )
                logging.debug("Response from Credit Scoring API: {}".format(response))
                if response.ok:
                    return response.json()
                raise response.raise_for_status()
            except Exception as e:
                if retries == max_retries - 1:
                    raise e
                retries += 1
                time.sleep(1)
                logging.debug("Retrying Credit Scoring API request: {}".format(e))
                continue

    def make_request_batch(self, wallets_addresses: dict) -> list:
        """Fetches wallet credit-scoring data from Spectral's API for a batch of wallets.

        Args:
            input (list): Request payload.
            workers (int): Number of workers to use for the concurrent requests.

        Returns:
            list: The response from the Credit-Scoring API.
        """
        max_retries = settings.NUM_RETRIES
        retries = 0
        while retries < max_retries:
            try:
                response = requests.post(
                    url=self.batch_url,
                    headers={"Authorization": f"bearer {self.api_key}", "Content-Type": "application/json"},
                    json={"wallet_addresses": wallets_addresses}
                )
                if not response.ok:
                    raise response.raise_for_status()
                market_data = response.json()['market_data']
                wallets_addresses_features = response.json()['wallets_addresses_features']
                for wallet_features in wallets_addresses_features:
                    wallet_features.update(market_data)
                return wallets_addresses_features
            except Exception as e:
                if retries == max_retries - 1:
                    raise e
                retries += 1
                time.sleep(1)
                logging.debug("Retrying Credit Scoring API request: {}".format(e))
                continue

    def request_batch(self, input: dict) -> list:
        """Fetches wallet credit-scoring data from Spectral's API for a batch of wallets.

        Args:
            input (dict): Request payload containing a list of wallet addresses.
            workers (int): Number of workers to use for the concurrent requests.

        Returns:
            list: The response from the Credit-Scoring API.
        """
        self.__validate_request_payload(input)
        requests_payload = []
        for i in range(0, len(input['wallets_addresses']), self.num_items_per_batch_request):
            requests_payload.append(input['wallets_addresses'][i: i + self.num_items_per_batch_request])

        responses = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            progress_bar = tqdm(total=len(requests_payload), desc="Processing requests", unit="request")

            futures_to_request_payload = {
                executor.submit(
                    self.make_request_batch,
                    request_payload
                ): request_payload for request_payload in requests_payload}

            for future in concurrent.futures.as_completed(futures_to_request_payload):
                try:
                    response = future.result()
                    responses.extend(response)
                except Exception as e:
                    logging.error(f"Request failed: {e}")
                    raise e
                finally:
                    progress_bar.update(1)

            progress_bar.close()

        if len(responses) != len(input['wallets_addresses']):
            logging.warning(f"Wallets features returned for {len(responses)} wallets, not matching the ({len(input['wallets_addresses'])}) requested wallet features")
        logging.info(f"Feature dataset successfully downloaded for {len(responses)} wallets!")

        return responses
